
import graphingFunctions as gf
import hexagon_utils as hex

#define side length of circumscribed hexagon (this is equal to the radius of the circle)
s = 2.5

#import border data and derivemax/min x/y values
border_data_X, border_data_Y = gf.getCSV('coordinates1964.csv')
x_max, x_min, y_max, y_min = gf.findBorders(border_data_X, border_data_Y)

hex_grid_x, hex_grid_y = hex.generate_hex_grid(x_min, x_max, y_min, y_max)

