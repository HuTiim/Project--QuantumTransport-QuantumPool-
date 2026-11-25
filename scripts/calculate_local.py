#!/usr/bin/env python3
"""Calcula densidade local e corrente pelas Eqs. R16--R22.

Este script não gera gráficos. Os resultados são escritos em data/local_*.npz.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import kwant
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def make_system(mask: np.ndarray, terminals: np.ndarray, normals: np.ndarray, lead_width: int):
    """Reconstrói o sistema aberto pela Eq. R2 e acopla seis leads pela Eq. R9."""
    lattice = kwant.lattice.square(norbs=1)
    height, width = mask.shape
    x_offset, y_offset = width // 2, height // 2
    cavity = kwant.Builder()

    def in_cavity(pos):
        mx = int(pos[0] + x_offset)
        my = int(pos[1] + y_offset)
        return 0 <= mx < width and 0 <= my < height and bool(mask[my, mx])

    active_y, active_x = np.nonzero(mask)
    start = (int(active_x[len(active_x) // 2]) - x_offset,
             int(active_y[len(active_y) // 2]) - y_offset)
    cavity[lattice.shape(in_cavity, start)] = 0.0
    cavity[lattice.neighbors()] = -1.0

    for terminal, normal in zip(terminals, normals):
        x, y = map(int, terminal)
        nx, ny = float(normal[0]), float(normal[1])
        if abs(nx) >= abs(ny):
            nx, ny = (1 if nx >= 0 else -1, 0)
        else:
            nx, ny = (0, 1 if ny >= 0 else -1)
        tx, ty = -ny, nx
        interface = []
        for offset in range(-(lead_width // 2), lead_width // 2 + 1):
            mx, my = x + offset * tx, y + offset * ty
            if 0 <= mx < width and 0 <= my < height and mask[my, mx]:
                interface.append(lattice(mx - x_offset, my - y_offset))
        symmetry = kwant.TranslationalSymmetry((nx, ny))
        lead = kwant.Builder(symmetry)
        for site in interface:
            lead[site] = 0.0
        lead[lattice.neighbors()] = -1.0
        cavity.attach_lead(lead)
    return cavity.finalized(), lattice


def _density_metrics(density: np.ndarray) -> tuple[float, float]:
    """Calcula normalização, índice de concentração R19 e centro de densidade."""
    total = float(np.sum(density))
    iniquity = float(np.sum(density**2) / (total**2)) if total > 0 else float("nan")
    center = float(np.sum(density) / total) if total > 0 else float("nan")
    return iniquity, center


def _flux_balance(current_operator, wavefunctions: np.ndarray) -> float:
    """Verifica balanço numérico médio dos estados do terminal injetor pela Eq. R21."""
    if wavefunctions.size == 0:
        return float("nan")
    residual = 0.0
    for psi in wavefunctions:
        residual += float(np.max(np.abs(np.asarray(current_operator(psi)))))
    return residual / len(wavefunctions)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--geometry", choices=("deformed",), default="deformed")
    parser.add_argument("--energy", type=float, default=0.25)
    parser.add_argument("--source", type=int, default=0)
    parser.add_argument("--lead-width", type=int, default=7)
    args = parser.parse_args()

    with np.load(DATA_DIR / "geometries.npz") as geometry:
        mask = geometry["mask"]
        terminals = geometry["terminals_lattice"]
        normals = geometry["terminal_normals"]

    system, lattice = make_system(mask, terminals, normals, args.lead_width)
    lead_count = len(system.leads)
    wave_function = kwant.wave_function(system, args.energy)
    current_operator = kwant.operator.Current(system)

    densities = np.zeros((lead_count, len(system.sites)), dtype=float)
    iniquities = np.zeros(lead_count, dtype=float)
    normalized_centers = np.zeros(lead_count, dtype=float)
    site_positions = np.asarray([site.pos for site in system.sites], dtype=float)

    hops = list(system.graph)
    link_positions = np.asarray([
        [system.sites[edge[0]].pos, system.sites[edge[1]].pos]
        for edge in hops
    ], dtype=float)
    current_links = np.zeros((lead_count, len(hops)), dtype=float)

    divergences = np.zeros((lead_count, len(system.sites)), dtype=float)

    for source in range(lead_count):
        wavefunctions = wave_function(source)
        density = np.sum(abs(wavefunctions) ** 2, axis=0)
        densities[source] = density
        iniquity, center = _density_metrics(density)
        iniquities[source] = iniquity
        normalized_centers[source] = center

        summed_current = np.zeros(len(hops), dtype=float)
        for psi in wavefunctions:
            link_values = np.asarray(current_operator(psi), dtype=float)
            summed_current += link_values[:len(hops)]
        current_links[source] = summed_current

        for link_index, edge in enumerate(hops):
            source_index = edge[0]
            target_index = edge[1]
            divergences[source, source_index] -= summed_current[link_index]
            divergences[source, target_index] += summed_current[link_index]

    height, width = mask.shape
    interface_positions = set(map(tuple, terminals))
    internal_indices = []
    for index, position in enumerate(site_positions):
        lattice_x = int(position[0] + width // 2)
        lattice_y = int(position[1] + height // 2)
        if (lattice_x, lattice_y) not in interface_positions:
            internal_indices.append(index)

    conservation_mean = np.mean(np.abs(divergences), axis=1)
    conservation_max = np.max(np.abs(divergences), axis=1)
    internal_mean = np.mean(np.abs(divergences[:, internal_indices]), axis=1)
    internal_max = np.max(np.abs(divergences[:, internal_indices]), axis=1)

    np.savez(
        DATA_DIR / f"local_{args.geometry}.npz",
        densities=densities,
        current_links=current_links,
        iniquities=iniquities,
        normalized_centers=normalized_centers,
        energy=np.asarray(args.energy),
        geometry=np.asarray(args.geometry),
        lead_count=np.asarray(lead_count),
        lattice_size=np.asarray(mask.shape),
        site_positions=site_positions,
        link_positions=link_positions,
        divergences=divergences,
        conservation_mean=conservation_mean,
        conservation_max=conservation_max,
        internal_mean=internal_mean,
        internal_max=internal_max,
    )
    print(f"Dados locais salvo em data/local_{args.geometry}.npz")


if __name__ == "__main__":
    main()
