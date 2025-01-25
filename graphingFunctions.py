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

def findBorders(col1 , col2):
    highest_x = col1.max()
    lowest_x = col1.min()
    highest_y = col2.max()
    lowest_y = col2.min()

    return highest_x, lowest_x, highest_y, lowest_y

def getPolygonFromPoints(col1, col2):
    points = list(zip(col1, col2))
    polygon = Polygon(points)
    return polygon

def isPointInside(polygon, x, y):
    point = Point(x, y)
    return polygon.contains(point)

#Plot a polygon and multiple points, coloring them based on whether they're inside or outside
#Done with the help of Claude AI
def plotPolygonWithPoints(polygon, points=None, inside_color='green', outside_color='red'):
    """
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

# Example usage:
if __name__ == "__main__":
    plotCSV("coordinates2011.csv" , "2011")
    # Create polygon from CSV
    col1, col2 = getCSV("coordinates2011.csv")
    polygon = getPolygonFromPoints(col1, col2)
    print(polygon.area)

