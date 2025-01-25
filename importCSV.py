<<<<<<< HEAD
test;
=======
import pandas as pd

def import_csv(file_name):
    # Load border data
    border_data = pd.read_csv(file_name)
    x_coords = border_data['x'].values
    y_coords = border_data['y'].values
    return border_data, x_coords, y_coords
>>>>>>> f7aa2cf5ddf51eccd402bbc1765c49fc8e2b98b2
