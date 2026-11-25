#!/usr/bin/env python3
"""Calcula observáveis relacionados aos seis leads pelas Eqs. R13--R22.

Este script não gera gráficos. Todas as tabelas são exportadas em `.npz`.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import kwant
import numpy as np

from calculate_local import make_system

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--e-min", type=float, default=-1.8)
    parser.add_argument("--e-max", type=float, default=1.8)
    parser.add_argument("--energy-count", type=int, default=37)
    parser.add_argument("--lead-width", type=int, default=7)
    args = parser.parse_args()

    with np.load(DATA_DIR / "geometries.npz") as geometry:
        mask = geometry["mask"]
        terminals = geometry["terminals_lattice"]
        normals = geometry["terminal_normals"]

    system, lattice = make_system(mask, terminals, normals, args.lead_width)
    energies = np.linspace(args.e_min, args.e_max, args.energy_count)
    lead_count = len(system.leads)

    transmissions = np.full((args.energy_count, lead_count, lead_count), np.nan)
    mode_counts = np.zeros((args.energy_count, lead_count), dtype=int)
    densities = np.zeros((args.energy_count, lead_count, len(system.sites)), dtype=float)
    iniquities = np.zeros((args.energy_count, lead_count), dtype=float)
    link_currents = None

    current_operator = kwant.operator.Current(system)

    for energy_index, energy in enumerate(energies):
        try:
            scattering = kwant.smatrix(system, float(energy))
            for source in range(lead_count):
                mode_counts[energy_index, source] = len(
                    system.leads[source].modes(float(energy))[0].momenta
                )
                for drain in range(lead_count):
                    transmissions[energy_index, drain, source] = scattering.transmission(drain, source)

            wave_function = kwant.wave_function(system, float(energy))
            for source in range(lead_count):
                wavefunctions = wave_function(source)
                density = np.sum(abs(wavefunctions) ** 2, axis=0)
                densities[energy_index, source] = density
                total = float(np.sum(density))
                iniquities[energy_index, source] = (
                    float(np.sum(density**2) / total**2) if total > 0 else np.nan
                )

                for psi in wavefunctions:
                    values = np.asarray(current_operator(psi), dtype=float)
                    if link_currents is None:
                        link_currents = np.zeros(
                            (args.energy_count, lead_count, values.size), dtype=float
                        )
                    link_currents[energy_index, source] += values
        except Exception:
            transmissions[energy_index] = np.nan
            mode_counts[energy_index] = 0

    if link_currents is None:
        link_currents = np.zeros((args.energy_count, lead_count, 0), dtype=float)

    outgoing = np.nansum(transmissions, axis=1)
    incoming = np.nansum(transmissions, axis=2)

    pair_names = np.asarray([
        f"T{source + 1}-T{drain + 1}"
        for source in range(lead_count)
        for drain in range(source + 1, lead_count)
    ])

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    np.savez(
        DATA_DIR / "lead_observables.npz",
        energies=energies,
        transmissions=transmissions,
        mode_counts=mode_counts,
        outgoing=outgoing,
        incoming=incoming,
        densities=densities,
        iniquities=iniquities,
        link_currents=link_currents,
        pair_names=pair_names,
        lead_count=np.asarray(lead_count),
        lead_width=np.asarray(args.lead_width),
        lattice_size=np.asarray(mask.shape),
        geometry=np.asarray("deformed"),
    )
    print("Observáveis dos seis leads salvo em data/lead_observables.npz")


if __name__ == "__main__":
    main()
