import numpy as np
import math 
#generate center points for a hexagon grid
def generate_hex_grid(x_min, x_max, y_min, y_max, s ,x_start, y_start):
    width = 3 * s
    height = np.sqrt(.5) * s

    # Create grid points
    x_coords = []
    y_coords = []
    
    x_width = math.floor((x_max - x_min) / width)+2
    y_height = math.floor((y_max - y_min) / height)+2
    if (y_height % 2 == 1):
        y_height += 1
    
    for y in range(y_height):
        for x in range(x_width):
            x_coords.append(x_start)
            y_coords.append(y_start)
           
            if (x_start > x_max):
                x_start -= x_width * width
            x_start += width

        x_start += width/2
        if (y_start > y_max):
            y_start -= y_height * height
        y_start += height

    return np.array(x_coords), np.array(y_coords)


#generate center points for a hexagon grid
#allows for a starting point and angle
#angle is in radians
#DOSENT WORK
def generate_hex_grid_optimized(x_min, x_max, y_min, y_max, s, start_x, start_y, angle):
    width = 2 * s
    height = np.sqrt(3) * s
    length = np.sqrt(width**2 + height**2)

    #so that it only moves up
    angle = angle % np.pi

    # Create grid points
    x_coords = []
    y_coords = []

    x = start_x
    y = start_y
    x_coords.append(start_x)
    y_coords.append(start_y)
    xx = x
    yy = y

    while (start_y > y_min-2*s) & (start_y < y_max+2*s):
        while (x < x_max + 2*s):
            y += height * np.sin(angle)
            x += width * np.cos(angle)
            x_coords.append(x)
            y_coords.append(y)

        x = start_x
        y = start_y

        while (x > x_min - 2*s):
            y -= height * np.sin(angle)
            x -= width * np.cos(angle)
            x_coords.append(x)
            y_coords.append(y)

        start_x = start_x + length * np.sin(angle)
        start_y = start_y + length * np.cos(angle)

    start_x = xx
    start_y = yy

    while (start_y > y_min-2*s) & (start_y < y_max+2*s):
        start_x = start_x - length * np.sin(angle)
        start_y = start_y - length * np.cos(angle)

        while (x < x_max + 2*s):
            y += height * np.sin(angle)
            x += width * np.cos(angle)
            x_coords.append(x)
            y_coords.append(y)
        
        x = start_x
        y = start_y

        while (x > x_min - 2*s):
            y -= height * np.sin(angle)
            x -= width * np.cos(angle)
            x_coords.append(x)
            y_coords.append(y)


    return np.array(x_coords), np.array(y_coords)