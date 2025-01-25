import graphingFunctions as gf
import hexagon_utils as hex

#define side length of circumscribed hexagon (this is equal to the radius of the circle)
s = 2.5

#import border data and derivemax/min x/y values
border_data_X, border_data_Y = gf.getCSV('coordinates1964.csv')
border_array = [border_data_X, border_data_Y]
border_tuples = set(zip(border_data_X, border_data_Y))
print(border_tuples)
x_max, x_min, y_max, y_min = gf.findBorders(border_data_X, border_data_Y)

hex_grid_x, hex_grid_y = hex.generate_hex_grid(x_min, x_max, y_min, y_max, s)

hex_grid = [hex_grid_x,hex_grid_y]
print(hex_grid)

polygon = gf.getPolygonFromPoints(border_data_X, border_data_Y)
print("\n\nprefin")
print(hex.greedy_hexagon_coverage(border_tuples, hex_grid, s))
print("\n\nfin")

#plt.plot(x, y, 'b-', label='Polygon Border')
