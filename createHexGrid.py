import numpy as np

#generate center points for a hexagon grid
def generate_hex_grid(x_min, x_max, y_min, y_max, s):
    width = 2 * s
    height = np.sqrt(3) * s

    # Create grid points
    x_coords = []
    y_coords = []

    for x in np.arange(x_min, x_max + width, width * 0.75):  # Horizontal shift by 3/4 width
        for y in np.arange(y_min, y_max + height, height):
            x_coords.append(x)
            y_coords.append(y)

            # Shift every other column
            if int((x - x_min) / width) % 2 == 1:
                y_coords[-1] += height / 2

    return np.array(x_coords), np.array(y_coords)


#generate center points for a hexagon grid
#allows for a starting point and angle
#angle is in radians
def generate_hex_grid_optimized(x_min, x_max, y_min, y_max, s, start_x, start_y, angle):
    width = 2 * s
    height = np.sqrt(3) * s

    # Create grid points
    x_coords = []
    y_coords = []

    x = start_x
    y = start_y
    x_coords.append(start_x)
    y_coords.append(start_y)
    xx = x
    yy = y
    while start_x>x_min-2*s & start_y>y_min-2*s:
        
        while y < y_max + 2*s & x < x_max + 2*s:
            y += 2*s * np.sin(angle)
            x += 2*s * np.cos(angle)
            x_coords.append(x)
            y_coords.append(y)

        x = start_x
        y = start_y
        while x > x_min - 2*s & y > y_min - 2*s:
            y -= 2*s * np.sin(angle)
            x -= 2*s * np.cos(angle)
            x_coords.append(x)
            y_coords.append(y)

        start_x = start_x + 2*s * np.sin(angle)
        start_y = start_y + 2*s * np.cos(angle)

    start_x = xx
    start_y = yy
    while start_x< x_max+2*s & start_y<y_max+2*s:

        start_x = start_x - 2*s * np.sin(angle)
        start_y = start_y - 2*s * np.cos(angle)

        while y < y_max + 2*s & x < x_max + 2*s:
            y += 2*s * np.sin(angle)
            x += 2*s * np.cos(angle)
            x_coords.append(x)
            y_coords.append(y)

        x = start_x
        y = start_y
        while x > x_min - 2*s & y > y_min - 2*s:
            y -= 2*s * np.sin(angle)
            x -= 2*s * np.cos(angle)
            x_coords.append(x)
            y_coords.append(y)

    return np.array(x_coords), np.array(y_coords)

# Define border bounding box
x_min, x_max = min(x_coords), max(x_coords)
y_min, y_max = min(y_coords), max(y_coords)

# Generate hexagonal grid with side length s
s = 1  # Example side length
hex_x, hex_y = generate_hex_grid(x_min, x_max, y_min, y_max, s)

# Define border bounding box
x_min, x_max = min(x_coords), max(x_coords)
y_min, y_max = min(y_coords), max(y_coords)

# Generate hexagonal grid with side length s
s = 1  # Example side length
hex_x, hex_y = generate_hex_grid(x_min, x_max, y_min, y_max, s)
