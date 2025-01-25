import pandas as pd

def findHighest(file_path):
    """
    Finds the highest, lowest x and y coordinates in kilometers from a CSV file containing (x, y) in kilometers.

    Args:
        file_path (str): Path to the CSV file containing x and y columns in kilometers.

    Returns:
        list: A list containing the highest x, lowest x, highest y, and lowest y values in that order.
    """
    # Load the data
    data = pd.read_csv(file_path)

    # Find the extremes
    highest_x = data['x'].max()
    lowest_x = data['x'].min()
    highest_y = data['y'].max()
    lowest_y = data['y'].min()

    return [highest_x, lowest_x, highest_y, lowest_y]