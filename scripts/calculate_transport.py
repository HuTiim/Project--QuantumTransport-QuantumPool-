#!/usr/bin/env python3
"""Calcula o transporte coerente do floco de neve deformado.

Referências: R1--R2, R10--R15 do DOCS/Report.md.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import kwant
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def snap_axis(normal: np.ndarray) -> tuple[int, int]:
    """Converte uma normal contínua em uma direção cardinal da lattice."""
    nx, ny = float(normal[0]), float(normal[1])
    if abs(nx) >= abs(ny):
        return (1 if nx >= 0 else -1, 0)
    return (0, 1 if ny >= 0 else -1)


def add_semi_infinite_leads(
    cavity: kwant.builder.Builder,
    lattice: kwant.lattice.MonatomicLattice,
    mask: np.ndarray,
    terminal_positions: np.ndarray,
    terminal_normals: np.ndarray,
    lead_width: int = 7,
) -> kwant.builder.FiniteSystem:
    """Acopla seis contatos semi-infinitos uniformes às interfaces da Eq. R9."""
    height, width = mask.shape
    x_offset = width // 2
    y_offset = height // 2

    for terminal, normal in zip(terminal_positions, terminal_normals):
        x, y = int(terminal[0]), int(terminal[1])
        nx, ny = snap_axis(normal)
        tx, ty = -ny, nx

        interface_sites = []
        for offset in range(-(lead_width // 2), lead_width // 2 + 1):
            mx = x + offset * tx
            my = y + offset * ty
            if 0 <= mx < width and 0 <= my < height and mask[my, mx]:
                interface_sites.append(lattice(mx - x_offset, my - y_offset))

        if not interface_sites:
            raise ValueError(f"Lead sem sítios de interface em ({x}, {y})")

        symmetry = kwant.TranslationalSymmetry((nx, ny))
        lead = kwant.Builder(symmetry)
        for site in interface_sites:
            lead[site] = 0.0
        lead[lattice.neighbors()] = -1.0
        cavity.attach_lead(lead)

    return cavity.finalized()


def make_cavity_from_mask(mask: np.ndarray) -> tuple[kwant.builder.Builder, kwant.lattice.MonatomicLattice]:
    """Reconstrói a cavidade como um sistema Kwant pela Eq. R2."""
    lattice = kwant.lattice.square(norbs=1)
    height, width = mask.shape
    cavity = kwant.Builder()

    def in_cavity(pos):
        mx = int(pos[0] + width // 2)
        my = int(pos[1] + height // 2)
        if 0 <= mx < width and 0 <= my < height:
            return bool(mask[my, mx])
        return False

    active_y, active_x = np.nonzero(mask)
    if active_x.size == 0:
        raise ValueError("Máscara da cavidade não contém sítios")

    start_x = int(active_x[active_x.size // 2]) - width // 2
    start_y = int(active_y[active_y.size // 2]) - height // 2
    cavity[lattice.shape(in_cavity, (start_x, start_y))] = 0.0
    cavity[lattice.neighbors()] = -1.0
    return cavity, lattice


def calculate_geometry(
    geometry_name: str,
    energies: np.ndarray,
    lead_width: int,
) -> dict[str, np.ndarray]:
    """Calcula transmissores $T_{mn}$ e condutâncias pelas Eqs. R14--R15."""
    with np.load(DATA_DIR / "geometries.npz") as geometry:
        mask = geometry["mask"]
        terminals = geometry["terminals_lattice"]
        normals = geometry["terminal_normals"]

    cavity, lattice = make_cavity_from_mask(mask)
    system = add_semi_infinite_leads(
        cavity, lattice, mask, terminals, normals, lead_width
    )

    lead_count = len(terminals)
    transmissions = np.zeros((energies.size, lead_count, lead_count), dtype=float)
    mode_counts = np.zeros((energies.size, lead_count), dtype=int)

    for index, energy in enumerate(energies):
        try:
            scattering = kwant.smatrix(system, float(energy))
            mode_counts[index] = [
                len(system.leads[lead].modes(float(energy))[0].momenta)
                for lead in range(lead_count)
            ]
            for source in range(lead_count):
                for drain in range(lead_count):
                    transmissions[index, drain, source] = scattering.transmission(drain, source)
        except Exception:
            transmissions[index, :, :] = np.nan
            mode_counts[index, :] = 0

    return {
        "energies": energies,
        "transmissions": transmissions,
        "mode_counts": mode_counts,
        "outgoing_per_source": np.nansum(transmissions, axis=1),
        "incoming_per_drain": np.nansum(transmissions, axis=2),
        "row_sums": np.nansum(transmissions, axis=1),
        "column_sums": np.nansum(transmissions, axis=2),
        "lead_width": np.asarray(lead_width),
        "geometry": np.asarray(geometry_name),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--geometry", choices=("deformed",), default="deformed")
    parser.add_argument("--e-min", type=float, default=-1.8)
    parser.add_argument("--e-max", type=float, default=1.8)
    parser.add_argument("--energy-count", type=int, default=37)
    parser.add_argument("--lead-width", type=int, default=7)
    args = parser.parse_args()

    if args.energy_count < 2:
        raise ValueError("--energy-count deve ser pelo menos 2")

    energies = np.linspace(args.e_min, args.e_max, args.energy_count)
    energies[np.abs(energies) < 1e-10] = np.nextafter(0.0, 1.0)
    result = calculate_geometry(args.geometry, energies, args.lead_width)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    np.savez(DATA_DIR / f"{args.geometry}.npz", **result)
    print(f"Transporte salvo em data/{args.geometry}.npz")


if __name__ == "__main__":
    main()
