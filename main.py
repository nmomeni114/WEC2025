import matplotlib.pyplot as plt
import graphingFunctions as gf
import hexagon_utils as hex
import createHexGrid as hg

#define side length of circumscribed hexagon (this is equal to the radius of the circle)
s = 2.5

#import border data and derivemax/min x/y values
border_data_X, border_data_Y = gf.getCSV('coordinates1964.csv')
x_max, x_min, y_max, y_min = gf.findBorders(border_data_X, border_data_Y)

hex_grid_x, hex_grid_y = hg.generate_hex_grid(x_min, x_max, y_min, y_max, s, 0 , 0)
#Shoutout to hpaulj for the zip
#hex_grid = zip(hex_grid_x,hex_grid_y)

polygon = gf.getPolygonFromPoints(border_data_X, border_data_Y)
# In your main.py
# Create test points (your hex grid points)
polygon = gf.getPolygonFromPoints(border_data_X, border_data_Y)
points = list(zip(hex_grid_x, hex_grid_y))
# Plot with circles of radius 2.5
wasted_area = gf.plotPolygonWithPoints(polygon, points, radius=2.5)
print(f"Total wasted area: {wasted_area}")
#hex.greedy_hexagon_coverage(polygon.exterior.xy, hex_grid, s)

plt.plot(hex_grid_x, hex_grid_y, 'r-', label='Hex Grid', marker = ".")
plt.plot(border_data_X, border_data_Y)
plt.xlabel('Longtitude (km)')
plt.ylabel('Latitude (km)')
plt.grid(True)
plt.show()

gf.plotPolygonWithPoints(polygon, set(zip(hex_grid_x, hex_grid_y)), 'green', 'red')
