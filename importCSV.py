import pandas as pd

# Load border data
border_data = pd.read_csv('border.csv')
x_coords = border_data['x'].values
y_coords = border_data['y'].values
