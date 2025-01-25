import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from shapely.geometry import Polygon, Point

def getPolygonFromCSV(file):
    current_dir = Path(__file__).parent
    csv_file = current_dir / file
    data = pd.read_csv(csv_file)

    # Get points as (x,y) pairs
    points = list(zip(data.iloc[:, 0], data.iloc[:, 1]))
    
    # Create polygon from points
    polygon = Polygon(points)
    return polygon

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

def isPointInside(polygon, x, y):
    point = Point(x, y)
    return polygon.contains(point)

# Example usage:
if __name__ == "__main__":
    # Create polygon from CSV
    polygon = getPolygonFromCSV("coordinates2011.csv")
    
    # Create some test points
    test_points = [
        Point(100, 100),
        Point(200, 200),
        Point(300, 300),
        # Add more points as needed
    ]
    
    # Plot the polygon with all points
    plotPolygonWithPoints(polygon, test_points) 