import numpy as np

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

# Define border bounding box
x_min, x_max = min(x_coords), max(x_coords)
y_min, y_max = min(y_coords), max(y_coords)

# Generate hexagonal grid with side length s
s = 1  # Example side length
hex_x, hex_y = generate_hex_grid(x_min, x_max, y_min, y_max, s)
