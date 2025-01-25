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
    plt.plot(col1, col2, '.', markersize=5)
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

#Plot a polygon and multiple circles, coloring them based on whether they're inside/intersecting
#Done with the help of Claude AI
def plotPolygonWithPoints(polygon, points=None, radius=2.5, inside_color='green', outside_color='red', year=''):
    """
    Plot a polygon and multiple circles, only showing those inside or intersecting the polygon
    
    Args:
        polygon: Shapely Polygon object
        points: List of (x,y) tuples or Point objects
        radius: Radius of the circles
        inside_color: Color for circles inside the polygon
        outside_color: Color for circles intersecting the polygon
        year: Year to display in the title
    """
    from matplotlib.patches import Circle
    from shapely.geometry import Point
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Plot polygon border
    x, y = polygon.exterior.xy
    plt.plot(x, y, '.', color='blue', markersize=5, label='Border Points')
    
    total_wasted_area = 0
    inside_count = 0
    intersecting_count = 0
    
    if points:
        # Convert points to circles and categorize them
        for p in points:
            if not isinstance(p, Point):
                p = Point(p)
            
            # Create Shapely circle
            circle = p.buffer(radius)
            
            # Only process circles that interact with the polygon
            if polygon.intersects(circle):
                if polygon.contains(circle):
                    # Circle completely inside
                    circle_patch = Circle((p.x, p.y), radius, alpha=0.3, 
                                       color=inside_color, label='Inside' if inside_count == 0 else "")
                    ax.add_patch(circle_patch)
                    inside_count += 1
                else:
                    # Circle intersects border
                    circle_patch = Circle((p.x, p.y), radius, alpha=0.3, 
                                       color=outside_color, label='Intersecting' if intersecting_count == 0 else "")
                    ax.add_patch(circle_patch)
                    intersecting_count += 1
                    
                    # Calculate and show wasted area
                    wasted_area = circle.difference(polygon)
                    if not wasted_area.is_empty:
                        total_wasted_area += wasted_area.area
                        # Plot the wasted area
                        if hasattr(wasted_area, 'exterior'):
                            x_waste, y_waste = wasted_area.exterior.xy
                            plt.fill(x_waste, y_waste, color='orange', alpha=0.5, 
                                   label='Wasted Area' if total_wasted_area == wasted_area.area else "")
    
    plt.grid(True)
    plt.axis('equal')  # Make circles appear circular
    plt.legend()
    total_circles = inside_count + intersecting_count
    title = f'Cowgary City Limits {year}\nTotal Circles: {total_circles} (Inside: {inside_count}, Intersecting: {intersecting_count})\nTotal Wasted Area: {total_wasted_area:.2f} square units'
    plt.title(title)
    plt.show()
    
    return total_wasted_area, inside_count, intersecting_count

def calculatePolygonCircles(polygon, points=None, radius=2.5):
    """
    Calculate metrics for circles within and intersecting a polygon without plotting
    
    Args:
        polygon: Shapely Polygon object
        points: List of (x,y) tuples or Point objects
        radius: Radius of the circles
    Returns:
        total_wasted_area: Area of circles outside the polygon
        inside_count: Number of circles completely inside
        intersecting_count: Number of circles intersecting the border
    """
    from shapely.geometry import Point
    
    total_wasted_area = 0
    inside_count = 0
    intersecting_count = 0
    
    if points:
        # Convert points to circles and categorize them
        for p in points:
            if not isinstance(p, Point):
                p = Point(p)
            
            # Create Shapely circle
            circle = p.buffer(radius)
            
            # Only process circles that interact with the polygon
            if polygon.intersects(circle):
                if polygon.contains(circle):
                    inside_count += 1
                else:
                    intersecting_count += 1
                    # Calculate wasted area
                    wasted_area = circle.difference(polygon)
                    if not wasted_area.is_empty:
                        total_wasted_area += wasted_area.area
    
    return total_wasted_area, inside_count, intersecting_count

if __name__ == "__main__":
    plotCSV("coordinates2011.csv" , "2011")
    plotCSV("coordinates2005.csv" , "2005")
    plotCSV("coordinates1964.csv" , "1964")


    # Create polygon from CSV
    col1, col2 = getCSV("coordinates2011.csv")
    polygon = getPolygonFromPoints(col1, col2)
    print(polygon.area)

