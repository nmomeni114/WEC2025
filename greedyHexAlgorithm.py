from shapely.geometry import Point, Polygon

def greedy_hexagon_coverage(border_points, hex_grid, hex_radius):
    uncovered_points = set(border_points)  # All border points
    selected_hexagons = []

    while uncovered_points:
        best_hexagon = None
        max_coverage = 0

        for hex_center in hex_grid:
            # Create a hexagon
            hexagon = create_hexagon(hex_center[0], hex_center[1], hex_radius)
            
            # Calculate coverage
            coverage = [p for p in uncovered_points if hexagon.contains(Point(p))]
            
            if len(coverage) > max_coverage:
                max_coverage = len(coverage)
                best_hexagon = hexagon

        if best_hexagon:
            # Add the best hexagon
            selected_hexagons.append(best_hexagon)

            # Remove covered points from the uncovered list
            uncovered_points = uncovered_points - set(
                [p for p in uncovered_points if best_hexagon.contains(Point(p))]
            )

    return selected_hexagons
