#!/usr/bin/env python3
"""Testa convergência da lattice e conservação da matriz S pelas Eqs. R13--R15."""

from __future__ import annotations

import sys
from pathlib import Path

import kwant
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
sys.path.insert(0, str(ROOT / "scripts"))

import build_geometries as geometry
import calculate_transport as transport


def build_resolution(size: int) -> tuple[np.ndarray, kwant.builder.FiniteSystem, np.ndarray, np.ndarray]:
    """Constrói uma única máscara do floco deformado e seis leads proporcionais."""
    lattice_size = (size, size)
    contour = geometry.snowflake_contour()
    contour_lattice = geometry.contour_to_lattice(contour, lattice_size)
    builder, lattice, mask, _ = geometry.make_kwant_cavity(contour_lattice, lattice_size)

    targets = geometry.uniform_terminal_targets()
    terminal_lattice = np.column_stack((
        np.round(targets[:, 0] * (size - 1)),
        np.round(targets[:, 1] * (size - 1)),
    )).astype(int)
    terminals, normals = geometry.project_terminals_to_boundary(mask, terminal_lattice)

    lead_width = max(5, round(7 * size / 120))
    cavity, lattice = transport.make_cavity_from_mask(mask)
    system = transport.add_semi_infinite_leads(
        cavity, lattice, mask, terminals, normals, lead_width
    )
    return mask, system, terminals, normals


def calculate_validation(size: int, energies: np.ndarray) -> dict[str, np.ndarray]:
    """Calcula transmissões, modos e resíduos unitários pela matriz S."""
    _, system, terminals, _ = build_resolution(size)
    lead_count = len(terminals)
    transmissions = np.full((energies.size, lead_count, lead_count), np.nan)
    mode_counts = np.zeros((energies.size, lead_count), dtype=int)
    scattering_norm = np.full(energies.size, np.nan)
    hermitian_norm = np.full(energies.size, np.nan)

    for energy_index, energy in enumerate(energies):
        try:
            scattering = kwant.smatrix(system, float(energy))

            s_matrix_parts = []
            for drain in range(lead_count):
                row_parts = []
                for source in range(lead_count):
                    row_parts.append(scattering.submatrix(drain, source))
                s_matrix_parts.append(np.hstack(row_parts))
            s_matrix = np.vstack(s_matrix_parts)

            scattering_norm[energy_index] = np.linalg.norm(
                s_matrix @ s_matrix.conj().T - np.eye(s_matrix.shape[0]), ord="fro"
            )
            hermitian_norm[energy_index] = np.linalg.norm(
                s_matrix.conj().T @ s_matrix - np.eye(s_matrix.shape[1]), ord="fro"
            )

            for source in range(lead_count):
                mode_counts[energy_index, source] = len(
                    system.leads[source].modes(float(energy))[0].momenta
                )
                for drain in range(lead_count):
                    transmissions[energy_index, drain, source] = (
                        scattering.transmission(drain, source)
                    )
        except Exception as error:
            if energy_index in (0, 18, 36):
                print(f"Falha {size} E={energy:.6g}: {error}")

    return {
        "energies": energies,
        "transmissions": transmissions,
        "mode_counts": mode_counts,
        "scattering_norm": scattering_norm,
        "hermitian_norm": hermitian_norm,
        "lattice_size": np.asarray(size),
    }


def main() -> None:
    energies = np.linspace(-1.8, 1.8, 37)
    energies[np.abs(energies) < 1e-10] = np.nextafter(0.0, 1.0)

    resolutions = (80, 120, 160)
    results = {}
    for size in resolutions:
        result = calculate_validation(size, energies)
        results[size] = result
        print(
            f"{size}: S†S-I médio={np.nanmean(result['scattering_norm']):.3e}, "
            f"máximo={np.nanmax(result['scattering_norm']):.3e}; "
            f"SS†-I médio={np.nanmean(result['hermitian_norm']):.3e}, "
            f"máximo={np.nanmax(result['hermitian_norm']):.3e}"
        )

    differences = {
        "difference_80_120": np.nanmean(
            np.abs(results[80]["transmissions"] - results[120]["transmissions"])
        ),
        "difference_120_160": np.nanmean(
            np.abs(results[120]["transmissions"] - results[160]["transmissions"])
        ),
    }

    np.savez(
        DATA_DIR / "convergence_validation.npz",
        energies=energies,
        resolution_80=results[80]["transmissions"],
        resolution_120=results[120]["transmissions"],
        resolution_160=results[160]["transmissions"],
        modes_80=results[80]["mode_counts"],
        modes_120=results[120]["mode_counts"],
        modes_160=results[160]["mode_counts"],
        residual_80=results[80]["scattering_norm"],
        residual_120=results[120]["scattering_norm"],
        residual_160=results[160]["scattering_norm"],
        hermitian_80=results[80]["hermitian_norm"],
        hermitian_120=results[120]["hermitian_norm"],
        hermitian_160=results[160]["hermitian_norm"],
        difference_80_120=np.asarray(differences["difference_80_120"]),
        difference_120_160=np.asarray(differences["difference_120_160"]),
    )
    print(f"Diferença média 80–120: {differences['difference_80_120']:.6e}")
    print(f"Diferença média 120–160: {differences['difference_120_160']:.6e}")
    print("Dados: data/convergence_validation.npz")


if __name__ == "__main__":
    main()
