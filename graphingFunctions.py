import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from shapely.geometry import Polygon, Point
import numpy as np
from matplotlib.patches import RegularPolygon

#Call function with "./coordinates1964.csv" ~ ensure that ./ is in it
def getCSV(file):
    current_dir = Path(__file__).parent
    csv_file = current_dir / file
    data = pd.read_csv(csv_file)
    print(data)
    
    latitudeScale = 69.85
    longitudeScale = 111
    
    col1 = data.iloc[:, 0]
    col2 = data.iloc[:, 1]
    col1 = (col1 + 114.09)*longitudeScale
    col2 = (col2 - 50.98)*latitudeScale
    return col1, col2

def plotCSV(file, title):
    col1, col2 = getCSV(file)
    plt.plot(col1, col2)
    plt.xlabel('Longtitude (km)')
    plt.ylabel('Latitude (km)')
    plt.title('Plot of ' + title + ' Cordinates')
    plt.grid(True)
    plt.show()

    return

def getPolygonFromPoints(col1, col2):
    points = list(zip(col1, col2))
    polygon = Polygon(points)
    return polygon

def insideBoundary(col1, col2, pointX, pointY):
    polygon = getPolygonFromPoints(col1, col2)
    return isPointInside(polygon, pointX, pointY)

def plotPolygonWithPoints(polygon, points=None, inside_color='green', outside_color='red'):
    """
    Plot a polygon and multiple points, coloring them based on whether they're inside or outside
    
    Args:
        polygon: Shapely Polygon object
        points: List of (x,y) tuples or Point objects
        inside_color: Color for points inside the polygon
        outside_color: Color for points outside the polygon
    """
    # Create figure
    plt.figure(figsize=(10, 10))
    
    # Plot polygon
    x, y = polygon.exterior.xy
    plt.plot(x, y, 'b-', label='Polygon Border')
    
    if points:
        # Convert all points to Point objects if they're not already
        points = [Point(p) if not isinstance(p, Point) else p for p in points]
        
        # Separate points into inside and outside
        inside_points = [p for p in points if polygon.contains(p)]
        outside_points = [p for p in points if not polygon.contains(p)]
        
        # Plot inside points
        if inside_points:
            x_in = [p.x for p in inside_points]
            y_in = [p.y for p in inside_points]
            plt.plot(x_in, y_in, 'o', color=inside_color, label='Inside Points')
            
        # Plot outside points
        if outside_points:
            x_out = [p.x for p in outside_points]
            y_out = [p.y for p in outside_points]
            plt.plot(x_out, y_out, 'o', color=outside_color, label='Outside Points')
    
    plt.grid(True)
    plt.legend()
    plt.show()

def create_hexagon(center, radius):
    """Create a Shapely polygon representing a hexagon"""
    angles = np.linspace(0, 2*np.pi, 7)[:-1]  # 6 points, excluding the repeated last point
    x = center[0] + radius * np.cos(angles)
    y = center[1] + radius * np.sin(angles)
    return Polygon(zip(x, y))

def isPointInside(polygon, x, y):
    point = Point(x, y)
    return polygon.contains(point)

def plotPolygonWithHexagons(polygon, points, hex_radius=10):
    """
    Plot a polygon with hexagons, highlighting those that intersect the border
    
    Args:
        polygon: Shapely Polygon object (the border)
        points: List of (x,y) tuples for hexagon centers
        hex_radius: Radius of the hexagons
    """
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Plot border polygon
    x, y = polygon.exterior.xy
    plt.plot(x, y, 'b-', label='Border', linewidth=2)
    
    # Categories for hexagons
    inside_hexagons = []
    outside_hexagons = []
    intersecting_hexagons = []
    wasted_area = 0
    
    # Create and categorize hexagons
    for point in points:
        hex_poly = create_hexagon((point[0], point[1]), hex_radius)
        
        if polygon.contains(hex_poly):
            inside_hexagons.append(hex_poly)
        elif not polygon.intersects(hex_poly):
            outside_hexagons.append(hex_poly)
        else:
            intersecting_hexagons.append(hex_poly)
            # Calculate wasted area (area of hexagon outside the polygon)
            if not polygon.contains(hex_poly):
                difference = hex_poly.difference(polygon)
                wasted_area += difference.area

    # Plot hexagons
    for hex_poly in inside_hexagons:
        x, y = hex_poly.exterior.xy
        plt.fill(x, y, alpha=0.3, color='green', label='Inside' if hex_poly == inside_hexagons[0] else "")
        
    for hex_poly in outside_hexagons:
        x, y = hex_poly.exterior.xy
        plt.fill(x, y, alpha=0.3, color='red', label='Outside' if hex_poly == outside_hexagons[0] else "")
        
    for hex_poly in intersecting_hexagons:
        x, y = hex_poly.exterior.xy
        plt.fill(x, y, alpha=0.3, color='yellow', label='Intersecting' if hex_poly == intersecting_hexagons[0] else "")
        
        # Highlight the wasted area
        difference = hex_poly.difference(polygon)
        if not difference.is_empty:
            x, y = difference.exterior.xy
            plt.fill(x, y, alpha=0.5, color='orange', 
                    label='Wasted Area' if hex_poly == intersecting_hexagons[0] else "")

    plt.grid(True)
    plt.legend()
    
    # Add wasted area information
    plt.title(f'Total Wasted Area: {wasted_area:.2f} square units')
    plt.axis('equal')
    plt.show()
    
    return wasted_area

def generate_hexagonal_grid(bounds, spacing):
    """Generate centers for a hexagonal grid within given bounds"""
    xmin, ymin, xmax, ymax = bounds
    
    # Horizontal spacing
    dx = spacing * 2
    # Vertical spacing
    dy = spacing * np.sqrt(3)
    
    x_coords = np.arange(xmin, xmax + dx, dx)
    y_coords = np.arange(ymin, ymax + dy, dy)
    
    points = []
    for i, y in enumerate(y_coords):
        for j, x in enumerate(x_coords):
            # Offset every other row
            if i % 2 == 0:
                points.append((x, y))
            else:
                points.append((x + spacing, y))
    
    return points

# Example usage:
if __name__ == "__main__":
    plotCSV("coordinates2011.csv" , "2011")
    # Create polygon from CSV
    col1, col2 = getCSV("coordinates2011.csv")
    polygon = getPolygonFromCSV(col1, col2)
    print(polygon.area)

