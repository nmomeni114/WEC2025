import matplotlib.pyplot as plt
import graphingFunctions as gf
import hexagon_utils as hex
import createHexGrid as hg
import numpy as np

#define side length of circumscribed hexagon (this is equal to the radius of the circle)
s = 2.5

#import border data and derivemax/min x/y values
border_data_X, border_data_Y = gf.getCSV('coordinates1964.csv')
x_max, x_min, y_max, y_min = gf.findBorders(border_data_X, border_data_Y)
hex_grid_x, hex_grid_y = hg.generate_hex_grid(x_min, x_max, y_min, y_max, s, 0 , 0)
polygon = gf.getPolygonFromPoints(border_data_X, border_data_Y)
points = list(zip(hex_grid_x, hex_grid_y))

# For plotting when needed
gf.plotPolygonWithPoints(polygon, points, radius=2.5, year='1964')

plt.plot(hex_grid_x, hex_grid_y, 'r-', label='Hex Grid', marker = ".")
plt.plot(border_data_X, border_data_Y)
plt.xlabel('Longtitude (km)')
plt.ylabel('Latitude (km)')
plt.grid(True)
plt.show()

border_data_X, border_data_Y = gf.getCSV('coordinates2005.csv')
x_max, x_min, y_max, y_min = gf.findBorders(border_data_X, border_data_Y)
hex_grid_x, hex_grid_y = hg.generate_hex_grid(x_min, x_max, y_min, y_max, s, 0 , 0)
polygon = gf.getPolygonFromPoints(border_data_X, border_data_Y)
points = list(zip(hex_grid_x, hex_grid_y))
wasted_area = gf.plotPolygonWithPoints(polygon, points, radius=2.5, year='2005')
print("Total wasted area: " + str(wasted_area))


border_data_X, border_data_Y = gf.getCSV('coordinates2011.csv')
x_max, x_min, y_max, y_min = gf.findBorders(border_data_X, border_data_Y)
hex_grid_x, hex_grid_y = hg.generate_hex_grid(x_min, x_max, y_min, y_max, s, 0 , 0)
polygon = gf.getPolygonFromPoints(border_data_X, border_data_Y)
points = list(zip(hex_grid_x, hex_grid_y))
wasted_area = gf.plotPolygonWithPoints(polygon, points, radius=2.5, year='2011')
print("Total wasted area: " + str(wasted_area))


##FIRST RUSHED ATTEMPT AT OPTIMIZATION
##MOVE UP AND DOWN AND LEFT AND RIGHT UNTIL THE WASTED AREA IS NO LONGER DECREASING
old_area = wasted_area[0]
area = wasted_area[0] 
x_pos = 0
y_pos = 0
i = 0
a = 0
b = 0
array = [] 

while i != 4:
    if i==0:
        x_pos += .2
        hex_grid_x, hex_grid_y = hg.generate_hex_grid(x_min, x_max, y_min, y_max, s, x_pos , y_pos)
        points = list(zip(hex_grid_x, hex_grid_y))
        wasted_area, inside, intersecting = gf.calculatePolygonCircles(polygon, points, radius=2.5)
        a += 1
        if (area > wasted_area): 
            x_pos -= .2
            i = 1
            a -= 1
    if i==1:
        y_pos += .2
        hex_grid_x, hex_grid_y = hg.generate_hex_grid(x_min, x_max, y_min, y_max, s, x_pos , y_pos)
        points = list(zip(hex_grid_x, hex_grid_y))
        wasted_area, inside, intersecting = gf.calculatePolygonCircles(polygon, points, radius=2.5)
        a += 1
        if (area > wasted_area):
            y_pos -= .2
            i = 2
            a -= 1
    if i==2:
        x_pos -= .2
        hex_grid_x, hex_grid_y = hg.generate_hex_grid(x_min, x_max, y_min, y_max, s, x_pos , y_pos)
        points = list(zip(hex_grid_x, hex_grid_y))
        wasted_area, inside, intersecting = gf.calculatePolygonCircles(polygon, points, radius=2.5)
        a += 1
        if (area > wasted_area):
            x_pos += .2
            i = 3
            a -= 1
    if i==3:
        y_pos -= .2
        hex_grid_x, hex_grid_y = hg.generate_hex_grid(x_min, x_max, y_min, y_max, s, x_pos , y_pos)
        points = list(zip(hex_grid_x, hex_grid_y))
        wasted_area, inside, intersecting = gf.calculatePolygonCircles(polygon, points, radius=2.5)
        a += 1
        if (area > wasted_area):
            y_pos += .2
            i = 4
            a -= 1
    if (a == b):
        break
    else:
        b = a
        i = 0
        array.append(str(wasted_area)) 
        if len(array) > 10 and (str(wasted_area) in array[-10:]):
            break
        print(a)

wasted_area, inside, intersecting = gf.calculatePolygonCircles(polygon, points, radius=2.5)
print("Total wasted area: " + str(wasted_area))
print("Area saved: " + str(old_area - wasted_area))  # Use the float values directly
print("Total stations: " + str(inside + intersecting))



##THIS OPTIMIZATION ALGORYTHEM IS DONE WITH THE HEP OF CLAUDE AI

print("\nStarting optimization...")

# Store initial configuration
best_wasted_area, best_inside, best_intersecting = gf.calculatePolygonCircles(polygon, points, radius=2.5)
best_x = 0
best_y = 0
best_total = best_inside + best_intersecting
initial_total = best_total

# Parameters for grid search
step_sizes = [2.0, 1.0, 0.5, 0.25]  # Larger initial steps
search_radius = 5.0  # Larger search radius
max_iterations = 20  # Fewer iterations per phase

# Calculate circle area for efficiency calculation
circle_area = np.pi * 2.5 * 2.5  # radius squared * pi

print(f"Initial configuration:")
print(f"Wasted area: {best_wasted_area:.2f}")
print(f"Total stations: {best_total}")
# Safe division for coverage efficiency
if best_total > 0 and circle_area > 0:
    efficiency = polygon.area / (best_total * circle_area)
    print(f"Coverage efficiency: {efficiency:.2%}")
else:
    print("Coverage efficiency: N/A (insufficient data)")

# Try each step size
for step_size in step_sizes:
    print(f"\nSearching with step size: {step_size}")
    no_improvement_count = 0
    
    while no_improvement_count < 5:  # Try 5 times before moving to next step size
        improved = False
        
        # Search in a grid pattern instead of spiral
        for x_offset in np.arange(-search_radius, search_radius + step_size, step_size):
            for y_offset in np.arange(-search_radius, search_radius + step_size, step_size):
                x = best_x + x_offset
                y = best_y + y_offset
                
                # Generate new grid with offset
                hex_grid_x, hex_grid_y = hg.generate_hex_grid(x_min, x_max, y_min, y_max, s, x, y)
                points = list(zip(hex_grid_x, hex_grid_y))
                
                # Calculate metrics
                current_wasted, inside, intersecting = gf.calculatePolygonCircles(polygon, points, radius=2.5)
                total_stations = inside + intersecting
                
                # Skip invalid configurations
                if total_stations == 0:
                    continue
                
                # Simplified improvement check
                if total_stations < best_total or (total_stations == best_total and current_wasted < best_wasted_area):
                    best_wasted_area = current_wasted
                    best_inside = inside
                    best_intersecting = intersecting
                    best_total = total_stations
                    best_x = x
                    best_y = y
                    improved = True
                    
                    print(f"\nImprovement found (step size: {step_size}):")
                    print(f"Offset: ({x:.2f}, {y:.2f})")
                    print(f"Total stations: {best_total} ({initial_total - best_total} fewer than initial)")
                    print(f"Wasted area: {best_wasted_area:.2f}")
                    # Safe division for coverage efficiency
                    if best_total > 0 and circle_area > 0:
                        efficiency = polygon.area / (best_total * circle_area)
                        print(f"Coverage efficiency: {efficiency:.2%}")
                    else:
                        print("Coverage efficiency: N/A (insufficient data)")
        
        if not improved:
            no_improvement_count += 1
        else:
            no_improvement_count = 0  # Reset counter if we found an improvement

# Generate final configuration
hex_grid_x, hex_grid_y = hg.generate_hex_grid(x_min, x_max, y_min, y_max, s, best_x, best_y)
points = list(zip(hex_grid_x, hex_grid_y))

print("\nOptimization complete!")
print(f"Best configuration found:")
print(f"Offset: ({best_x:.2f}, {best_y:.2f})")
print(f"Inside stations: {best_inside}")
print(f"Intersecting stations: {best_intersecting}")
print(f"Total stations: {best_total} ({initial_total - best_total} fewer than initial)")
print(f"Wasted area: {best_wasted_area:.2f}")
# Safe division for final coverage efficiency
if best_total > 0 and circle_area > 0:
    efficiency = polygon.area / (best_total * circle_area)
    print(f"Coverage efficiency: {efficiency:.2%}")
else:
    print("Coverage efficiency: N/A (insufficient data)")

# Plot final configuration
gf.plotPolygonWithPoints(polygon, points, radius=2.5, year='2011 (Optimized)')


