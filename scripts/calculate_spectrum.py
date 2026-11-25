#!/usr/bin/env python3
"""Calcula os espectros fechados das geometrias de floco de neve.

Referências: Hamiltoniano R1--R2 e diagonalização R23--R26 do
DOCS/Report.md. Este script realiza apenas cálculo e escrita em NPZ.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import kwant
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def spectrum_from_mask(mask: np.ndarray, count: int) -> tuple[np.ndarray, np.ndarray]:
    """Constrói o Hamiltoniano fechado e calcula os menores valores pela Eq. R23."""
    lattice = kwant.lattice.square(norbs=1)
    height, width = mask.shape
    system = kwant.Builder()

    def in_cavity(pos):
        mx = int(pos[0] + width // 2)
        my = int(pos[1] + height // 2)
        return 0 <= mx < width and 0 <= my < height and bool(mask[my, mx])

    active_y, active_x = np.nonzero(mask)
    if active_x.size == 0:
        raise ValueError("Máscara vazia")
    start = (int(active_x[len(active_x) // 2]) - width // 2,
             int(active_y[len(active_y) // 2]) - height // 2)
    system[lattice.shape(in_cavity, start)] = 0.0
    system[lattice.neighbors()] = -1.0

    finalized = system.finalized()
    hamiltonian = finalized.hamiltonian_submatrix()
    eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian)
    count = min(count, eigenvalues.size)
    return eigenvalues[:count], eigenvectors[:, :count]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=120)
    args = parser.parse_args()

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with np.load(DATA_DIR / "geometries.npz") as geometry:
        eigenvalues, eigenvectors = spectrum_from_mask(
            geometry["mask"], args.count
        )
        np.savez(
            DATA_DIR / "spectrum_deformed.npz",
            eigenvalues=eigenvalues,
            eigenvectors=eigenvectors,
            spacing=np.diff(eigenvalues),
            geometry=np.asarray("deformed"),
        )
        print("Espectro salvo em data/spectrum_deformed.npz")


if __name__ == "__main__":
    main()
