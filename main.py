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
polygon = gf.getPolygonFromPoints(border_data_X, border_data_Y)
points = list(zip(hex_grid_x, hex_grid_y))
wasted_area, inside, intersecting = gf.plotPolygonWithPoints(polygon, points, radius=2.5, year='1964')
print(f"Total wasted area: {wasted_area}")
print(f"Inside circles: {inside}")
print(f"Intersecting circles: {intersecting}")
print(f"Total circles: {inside + intersecting}")

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