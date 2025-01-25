import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from shapely.geometry import Polygon, Point, circle
import numpy as np
from matplotlib.patches import Circle

def getPolygonFromCSV(file):
    current_dir = Path(__file__).parent
    csv_file = current_dir / file
    data = pd.read_csv(csv_file)
    points = list(zip(data.iloc[:, 0], data.iloc[:, 1]))
    polygon = Polygon(points)
    return polygon

def create_circle(center, radius):
    """Create a Shapely circle"""
    return Point(center).buffer(radius)

def circles_overlap(c1_center, c2_center, radius):
    """Check if two circles overlap"""
    return np.sqrt((c1_center[0] - c2_center[0])**2 + 
                   (c1_center[1] - c2_center[1])**2) < 2*radius

def find_optimal_circle_packing(polygon, radius):
    """
    Find optimal circle packing within polygon using a grid-based approach
    with iterative refinement
    """
    bounds = polygon.bounds
    min_x, min_y, max_x, max_y = bounds
    
    # Initial grid spacing slightly less than diameter to ensure coverage
    spacing = radius * 1.9  
    
    circles = []
    centers = []
    
    # Create initial triangular grid for better packing
    y = min_y
    row = 0
    while y <= max_y:
        x = min_x + (row % 2) * (spacing/2)  # Offset alternate rows
        while x <= max_x:
            center = (x, y)
            circle = create_circle(center, radius)
            
            # Check if circle is within or intersects polygon
            if polygon.contains(circle) or polygon.intersects(circle):
                # Check overlap with existing circles
                overlaps = False
                for existing_center in centers:
                    if circles_overlap(center, existing_center, radius):
                        overlaps = True
                        break
                
                if not overlaps:
                    circles.append(circle)
                    centers.append(center)
            
            x += spacing
        y += spacing * np.sqrt(3)/2  # Height of equilateral triangle
        row += 1
    
    return circles

def plotPolygonWithCircles(polygon, circles):
    """Plot polygon border and packed circles"""
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Plot border
    x, y = polygon.exterior.xy
    plt.plot(x, y, 'b-', label='Border', linewidth=2)
    
    # Plot circles
    for circle in circles:
        x, y = circle.centroid.coords[0]
        radius = np.sqrt(circle.area / np.pi)  # Get radius from area
        
        if polygon.contains(circle):
            color = 'green'
            alpha = 0.3
        else:
            color = 'yellow'
            alpha = 0.3
            # Calculate and show wasted area
            difference = circle.difference(polygon)
            if not difference.is_empty:
                diff_x, diff_y = difference.exterior.xy
                plt.fill(diff_x, diff_y, alpha=0.5, color='orange')
    
        circle_patch = Circle((x, y), radius, alpha=alpha, color=color)
        ax.add_patch(circle_patch)
    
    plt.grid(True)
    plt.axis('equal')
    plt.legend(['Border', 'Inside Circles', 'Intersecting Circles', 'Wasted Area'])
    
    # Calculate coverage metrics
    total_circle_area = sum(circle.area for circle in circles)
    intersection_area = sum(circle.intersection(polygon).area for circle in circles)
    wasted_area = total_circle_area - intersection_area
    coverage_ratio = intersection_area / polygon.area
    
    plt.title(f'Circle Packing\nCoverage: {coverage_ratio:.2%}\nWasted Area: {wasted_area:.2f}')
    plt.show()
    
    return coverage_ratio, wasted_area

if __name__ == "__main__":
    # Create polygon from CSV
    polygon = getPolygonFromCSV("coordinates2011.csv")
    
    # Try different radii to find optimal packing
    radius = 10  # Starting radius - adjust this value
    
    # Pack circles
    circles = find_optimal_circle_packing(polygon, radius)
    
    # Plot results
    coverage_ratio, wasted_area = plotPolygonWithCircles(polygon, circles)
    print(f"Coverage ratio: {coverage_ratio:.2%}")
    print(f"Wasted area: {wasted_area:.2f}")