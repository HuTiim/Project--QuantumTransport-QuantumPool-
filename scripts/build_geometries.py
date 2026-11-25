#!/usr/bin/env python3
"""Constrói exclusivamente o floco de neve deformado em Kwant.

Referências: contorno R3--R6, lattice R7, terminais R8--R9 do
DOCS/Report.md. Este script realiza apenas cálculo numérico e escrita de dados.
"""

from __future__ import annotations

import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import kwant
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SVG_PATH = ROOT / "inomeado.svg"
DATA_DIR = ROOT / "data"

TERMINAL_NAMES = tuple(f"terminal_{index}" for index in range(1, 7))
LEAD_COUNT = 6


def _rotate_point(point: np.ndarray, angle_deg: float) -> np.ndarray:
    """Aplica uma rotação 2D em torno da origem, conforme o SVG."""
    angle = math.radians(angle_deg)
    rotation = np.array(
        [[math.cos(angle), -math.sin(angle)],
         [math.sin(angle), math.cos(angle)]],
        dtype=float,
    )
    return rotation @ point


def parse_svg_rects(svg_path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Extrai centros, dimensões e orientações dos terminais azuis (Eqs. R8--R9)."""
    root = ET.parse(svg_path).getroot()
    ns = {"svg": "http://www.w3.org/2000/svg"}
    viewbox = tuple(map(float, root.attrib["viewBox"].split()))

    terminals: list[np.ndarray] = []
    dimensions: list[np.ndarray] = []
    angles: list[float] = []

    for rect in root.findall(".//svg:rect", ns):
        style = rect.attrib.get("style", "")
        if "#0000ff" not in style.lower() and "blue" not in style.lower():
            continue

        x = float(rect.attrib["x"])
        y = float(rect.attrib["y"])
        width = float(rect.attrib["width"])
        height = float(rect.attrib["height"])
        angle = 0.0

        transform = rect.attrib.get("transform", "")
        match = re.search(r"rotate\(([-+0-9.eE]+)", transform)
        if match:
            angle = float(match.group(1))

        if angle:
            center_before = np.array([x + width / 2.0, y + height / 2.0])
            center = _rotate_point(center_before, angle)
        else:
            center = np.array([x + width / 2.0, y + height / 2.0])

        terminals.append(center)
        dimensions.append(np.array([width, height]))
        angles.append(angle)

    if len(terminals) != 3:
        raise ValueError(f"Esperados 3 terminais azuis; encontrados {len(terminals)}")

    return (
        np.asarray(terminals, dtype=float),
        np.asarray(viewbox, dtype=float),
        np.asarray(dimensions, dtype=float),
        np.asarray(angles, dtype=float),
    )


def _flatten_svg_path(d: str, samples_per_segment: int = 16) -> np.ndarray:
    """Converte os comandos M/L/C/Z relevantes do SVG em vértices amostrados."""
    command_tokens = re.findall(
        r"[MLHVCSQTAZmlhvcsqtaz]|[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]\d+)?",
        d,
    )

    points: list[np.ndarray] = []
    current = np.zeros(2, dtype=float)
    subpath_start = np.zeros(2, dtype=float)
    command = None
    index = 0

    def read_numbers(count: int) -> list[float]:
        nonlocal index
        values: list[float] = []
        while len(values) < count and index < len(command_tokens):
            token = command_tokens[index]
            if re.fullmatch(r"[MLHVCSQTAZmlhvcsqtaz]", token):
                break
            values.append(float(token))
            index += 1
        return values

    while index < len(command_tokens):
        token = command_tokens[index]
        if re.fullmatch(r"[MLHVCSQTAZmlhvcsqtaz]", token):
            command = token
            index += 1
            continue

        if command is None:
            raise ValueError("Dados SVG sem comando inicial")

        relative = command.islower()
        letter = command.upper()

        if letter == "M":
            values = read_numbers(2)
            if len(values) != 2:
                break
            delta = np.asarray(values, dtype=float)
            current = subpath_start = current + delta if relative else delta
            points.append(current.copy())
            command = "l" if relative else "L"

        elif letter == "L":
            values = read_numbers(2)
            if len(values) != 2:
                break
            delta = np.asarray(values, dtype=float)
            current = current + delta if relative else delta
            points.append(current.copy())

        elif letter == "C":
            values = read_numbers(6)
            if len(values) != 6:
                break
            if relative:
                raw = np.asarray(values, dtype=float).reshape(3, 2)
                control1 = current + raw[0]
                control2 = current + raw[1]
                end = current + raw[2]
            else:
                raw = np.asarray(values, dtype=float).reshape(3, 2)
                control1, control2, end = raw

            t = np.linspace(0.0, 1.0, samples_per_segment + 1)[1:, None]
            p0 = current
            cubic = (
                ((1.0 - t) ** 3) * p0
                + 3.0 * ((1.0 - t) ** 2) * t * control1
                + 3.0 * (1.0 - t) * (t ** 2) * control2
                + (t ** 3) * end
            )
            points.extend(cubic)
            current = end

        elif letter == "Z":
            if np.linalg.norm(current - subpath_start) > 1e-12:
                points.append(subpath_start.copy())
            break

        else:
            raise ValueError(f"Comando SVG não suportado nesta etapa: {letter}")

    if not points:
        raise ValueError("O contorno SVG não produziu vértices")
    return np.asarray(points, dtype=float)


def parse_svg_contour(svg_path: Path) -> np.ndarray:
    """Extrai o contorno preto principal do SVG e o amostra em pontos."""
    root = ET.parse(svg_path).getroot()
    ns = {"svg": "http://www.w3.org/2000/svg"}

    for path in root.findall(".//svg:path", ns):
        d = path.attrib.get("d")
        style = path.attrib.get("style", "")
        if d and "stroke:#000000" in style:
            return _flatten_svg_path(d)

    raise ValueError("Contorno preto não encontrado em inomeado.svg")


def normalize_points(points: np.ndarray, viewbox: np.ndarray) -> np.ndarray:
    """Normaliza coordenadas para [0,1] e inverte o eixo vertical do SVG."""
    _, _, width, height = viewbox
    normalized = np.empty_like(points, dtype=float)
    normalized[:, 0] = points[:, 0] / width
    normalized[:, 1] = 1.0 - points[:, 1] / height
    return normalized


def point_in_polygon(points: np.ndarray, polygon: np.ndarray) -> np.ndarray:
    """Testa quais pontos da lattice estão dentro do contorno fechado."""
    px = points[:, 0]
    py = points[:, 1]
    x = polygon[:, 0]
    y = polygon[:, 1]
    x_next = np.roll(x, -1)
    y_next = np.roll(y, -1)

    crossing_x = np.empty((polygon.shape[0], points.shape[0]), dtype=float)
    for edge in range(polygon.shape[0]):
        dy = y_next[edge] - y[edge]
        if abs(dy) < 1e-12:
            crossing_x[edge] = np.inf
        else:
            crossing_x[edge] = x[edge] + (py - y[edge]) * (x_next[edge] - x[edge]) / dy

    crosses = ((y[:, None] > py[None, :]) != (y_next[:, None] > py[None, :]))
    inside = np.sum(crosses & (px[None, :] < crossing_x), axis=0) % 2 == 1
    return inside


def smooth_contour(deformed: np.ndarray, n_harmonics: int = 7) -> np.ndarray:
    """Produz o contorno regular suavizando harmônicos da deformação (Eqs. R3--R5)."""
    center = deformed.mean(axis=0)
    dx = deformed[:, 0] - center[0]
    dy = deformed[:, 1] - center[1]
    angle = np.arctan2(dy, dx)
    radius = np.hypot(dx, dy)

    order = np.argsort(angle)
    angle = angle[order]
    radius = radius[order]

    angle_full = np.concatenate((angle - 2.0 * math.pi, angle, angle + 2.0 * math.pi))
    radius_full = np.concatenate((radius, radius, radius))

    sample_angle = np.linspace(-math.pi, math.pi, 721, endpoint=False)
    smooth_radius = np.interp(sample_angle, angle_full, radius_full)

    coefficients = np.fft.rfft(smooth_radius)
    coefficients[n_harmonics + 1:] = 0.0
    coefficients[1:n_harmonics + 1] *= 0.30
    smooth_radius = np.fft.irfft(coefficients, n=sample_angle.size)

    contour = np.column_stack(
        (center[0] + smooth_radius * np.cos(sample_angle),
         center[1] + smooth_radius * np.sin(sample_angle))
    )
    return contour


def contour_to_lattice(contour: np.ndarray, lattice_size: tuple[int, int]) -> np.ndarray:
    """Escala coordenadas normalizadas para os índices inteiros da lattice."""
    width, height = lattice_size
    return np.column_stack(
        (contour[:, 0] * (width - 1), contour[:, 1] * (height - 1))
    )


def make_kwant_cavity(contour_lattice: np.ndarray, lattice_size: tuple[int, int]):
    """Cria o sistema de cavidade quadrada em Kwant pela Eq. R2 do relatório."""
    lattice = kwant.lattice.square(norbs=1)
    builder = kwant.Builder()
    width, height = lattice_size

    xs, ys = np.meshgrid(np.arange(width), np.arange(height), indexing="xy")
    lattice_points = np.column_stack((xs.ravel(), ys.ravel()))
    offsets = np.array([-width // 2, -height // 2], dtype=int)
    points = lattice_points + offsets

    selected = point_in_polygon(lattice_points, contour_lattice)

    def in_cavity(pos):
        mx = int(pos[0] + width // 2)
        my = int(pos[1] + height // 2)
        if 0 <= mx < width and 0 <= my < height:
            index = my * width + mx
            return bool(selected[index])
        return False

    active_indices = np.flatnonzero(selected)
    if active_indices.size == 0:
        raise ValueError("O contorno não contém sítios da lattice")
    index = int(active_indices[len(active_indices) // 2])
    start_x = int(lattice_points[index, 0])
    start_y = int(lattice_points[index, 1])

    center = (start_x - width // 2, start_y - height // 2)
    builder[lattice.shape(in_cavity, center)] = 0.0
    builder[lattice.neighbors()] = -1.0

    return builder, lattice, selected.reshape((height, width)), points


def write_geometry_svg(output_path: Path, regular: np.ndarray, deformed: np.ndarray,
                       terminals: np.ndarray) -> None:
    """Exporta contornos e terminais normalizados em formato SVG."""

    def path_data(contour: np.ndarray) -> str:
        points = np.column_stack((contour[:, 0] * 400.0,
                                  (1.0 - contour[:, 1]) * 400.0))
        commands = [f"M {points[0, 0]:.3f} {points[0, 1]:.3f}"]
        commands.extend(f"L {x:.3f} {y:.3f}" for x, y in points[1:])
        commands.append("Z")
        return " ".join(commands)

    terminal_rects = []
    for x, y in terminals:
        terminal_rects.append(
            f'<rect x="{x * 400.0 - 7:.3f}" y="{(1.0 - y) * 400.0 - 3:.3f}" '
            'width="14" height="6" fill="#0000ff" stroke="#0000ff"/>'
        )

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" '
        'viewBox="0 0 400 400">\n'
        '<rect width="400" height="400" fill="white"/>\n'
        f'<path d="{path_data(regular)}" fill="none" stroke="#111111" '
        'stroke-width="3"/>\n'
        f'<path d="{path_data(deformed)}" fill="none" stroke="#d62728" '
        'stroke-width="2" stroke-dasharray="6 4"/>\n'
        + "\n".join(terminal_rects)
        + "\n</svg>\n"
    )
    output_path.write_text(svg, encoding="utf-8")


def project_terminals_to_boundary(mask: np.ndarray, target_points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Projeta os terminais sobre sítios físicos da borda (Eq. R9 do relatório)."""
    height, width = mask.shape
    ys, xs = np.indices(mask.shape)

    outside = np.zeros_like(mask, dtype=bool)
    outside[1:, :] |= ~mask[:-1, :]
    outside[:-1, :] |= ~mask[1:, :]
    outside[:, 1:] |= ~mask[:, :-1]
    outside[:, :-1] |= ~mask[:, 1:]
    boundary = mask & outside

    boundary_positions = np.column_stack((xs[boundary], ys[boundary]))
    projected: list[np.ndarray] = []
    normals: list[np.ndarray] = []

    for target in target_points:
        distances = np.sum((boundary_positions - target) ** 2, axis=1)
        point = boundary_positions[int(np.argmin(distances))]
        x, y = int(point[0]), int(point[1])
        projected.append(point.copy())

        normal = np.zeros(2, dtype=int)
        if x > 0 and not mask[y, x - 1]:
            normal[0] -= 1
        if x + 1 < width and not mask[y, x + 1]:
            normal[0] += 1
        if y > 0 and not mask[y - 1, x]:
            normal[1] -= 1
        if y + 1 < height and not mask[y + 1, x]:
            normal[1] += 1
        if normal.sum() == 0:
            normal = np.array([0, 1], dtype=int)
        normal = normal / max(np.linalg.norm(normal), 1.0)
        normals.append(normal)

    return np.asarray(projected, dtype=int), np.asarray(normals, dtype=float)


def snowflake_contour(n: int = 721) -> np.ndarray:
    """Gera o contorno principal deformado de floco de neve pelas Eqs. R3--R6."""
    theta = np.linspace(-math.pi, math.pi, n, endpoint=False)
    radius = 0.20 * (
        1.0
        + 0.55 * np.cos(6.0 * theta)
        + 0.22 * np.cos(18.0 * theta)
        + 0.12 * np.cos(24.0 * theta)
    )
    return np.column_stack((0.5 + radius * np.cos(theta),
                            0.5 + radius * np.sin(theta)))


def uniform_terminal_targets() -> np.ndarray:
    """Define seis leads uniformemente distribuídos a 60 graus pela Eq. R8."""
    angle = np.deg2rad(np.arange(6) * 60.0)
    radius = 0.25
    return np.column_stack((0.5 + radius * np.cos(angle),
                            0.5 + radius * np.sin(angle)))


def main(lattice_size: tuple[int, int] = (120, 120), deformation_scale: float = 1.0) -> None:
    """Constrói exclusivamente o floco deformado e salva máscaras pelas Eqs. R2 e R7--R9."""
    width, height = lattice_size
    terminals_normalized = uniform_terminal_targets()
    deformed = snowflake_contour()
    deformed_lattice = contour_to_lattice(deformed, lattice_size)

    deformed_builder, lattice, deformed_mask, deformed_points = make_kwant_cavity(
        deformed_lattice, lattice_size
    )
    deformed_sites = sum(1 for _ in deformed_builder.sites())

    terminal_lattice = np.column_stack(
        (np.round(terminals_normalized[:, 0] * (width - 1)),
         np.round(terminals_normalized[:, 1] * (height - 1)))
    ).astype(int)
    terminal_lattice, terminal_normals = project_terminals_to_boundary(
        deformed_mask, terminal_lattice
    )

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    np.savez(
        DATA_DIR / "geometries.npz",
        contour=deformed,
        mask=deformed_mask,
        terminals_normalized=terminals_normalized,
        terminals_lattice=terminal_lattice,
        terminal_normals=terminal_normals,
        terminal_names=np.asarray(TERMINAL_NAMES),
        terminal_dimensions=np.asarray([[7.0, 7.0]] * LEAD_COUNT),
        terminal_angles=np.rad2deg(np.arange(LEAD_COUNT) * 2.0 * math.pi / LEAD_COUNT),
        lattice_size=np.asarray(lattice_size),
        lattice_vectors=np.asarray(lattice.prim_vecs),
        hopping=-1.0,
        onsite=0.0,
        deformation_scale=float(deformation_scale),
        site_count=np.asarray(deformed_sites),
    )

    write_geometry_svg(DATA_DIR / "geometries.svg", deformed,
                       deformed, terminals_normalized)

    print(f"Lattice: {width} x {height}")
    print(f"Sítios do floco deformado: {deformed_sites}")
    print("Dados: data/geometries.npz")
    print("Contorno: data/geometries.svg")


if __name__ == "__main__":
    main()
