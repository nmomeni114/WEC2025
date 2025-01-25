# hexagon_utils.py

import numpy as np
from shapely.geometry import Point, Polygon

def generate_hex_grid(x_min, x_max, y_min, y_max, s):
    """
    Generates a hexagonal grid of points.

    Parameters:
        x_min, x_max, y_min, y_max: Bounds of the grid
        s: Side length of each hexagon

    Returns:
        Two lists of x and y coordinates for hexagon centers
    """
    width = 2 * s
    height = np.sqrt(3) * s

    x_coords = []
    y_coords = []

    for x in np.arange(x_min, x_max + width, width * 0.75):
        for y in np.arange(y_min, y_max + height, height):
            x_coords.append(x)
            y_coords.append(y)

            if int((x - x_min) / width) % 2 == 1:
                y_coords[-1] += height / 2

    return np.array(x_coords), np.array(y_coords)


def create_hexagon(center_x, center_y, s):
    """
    Creates a hexagon as a Shapely Polygon.

    Parameters:
        center_x, center_y: Center of the hexagon
        s: Side length of the hexagon

    Returns:
        A Shapely Polygon representing the hexagon
    """
    angles = np.linspace(0, 2 * np.pi, 7)
    x_hex = center_x + s * np.cos(angles)
    y_hex = center_y + s * np.sin(angles)
    return Polygon(zip(x_hex, y_hex))

def greedy_hexagon_coverage(border_points, hex_grid, s):
    """
    Greedy algorithm to find the minimal number of hexagons for full coverage.

    Parameters:
        border_points: List of (x, y) points defining the border
        hex_grid: List of (x, y) hexagon centers
        s: Side length of the hexagons

    Returns:
        List of Shapely Polygons representing the selected hexagons
    """
    uncovered_points = set(border_points)
    selected_hexagons = []

    while uncovered_points:
        best_hexagon = None
        max_coverage = 0

        for hx, hy in hex_grid:
            hexagon = create_hexagon(hx, hy, s)
            coverage = [p for p in uncovered_points if hexagon.contains(Point(p))]

            if len(coverage) > max_coverage:
                max_coverage = len(coverage)
                best_hexagon = hexagon

        if best_hexagon:
            selected_hexagons.append(best_hexagon)
            # Remove covered points from the uncovered set
            uncovered_points -= set([p for p in uncovered_points if best_hexagon.contains(Point(p))])

    return selected_hexagons