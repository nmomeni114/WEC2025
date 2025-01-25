import pandas as pd

def find_border_extremes_and_center(file_path):
    """
    Finds the highest and lowest latitude and longitude in the CSV file
    and calculates the center point.

    Args:
        file_path (str): Path to the CSV file containing Latitude and Longitude columns.

    Returns:
        dict: Dictionary containing highest and lowest latitude and longitude,
              and the center latitude and longitude.
    """
    # Load the data
    data = pd.read_csv(file_path)

    # Find the extremes
    highest_latitude = data['Latitude'].max()
    lowest_latitude = data['Latitude'].min()
    highest_longitude = data['Longitude'].max()
    lowest_longitude = data['Longitude'].min()

    # Calculate the center point
    center_latitude = (highest_latitude + lowest_latitude) / 2
    center_longitude = (highest_longitude + lowest_longitude) / 2

    # Return the results
    return {
        'Highest Latitude': highest_latitude,
        'Lowest Latitude': lowest_latitude,
        'Highest Longitude': highest_longitude,
        'Lowest Longitude': lowest_longitude,
        'Center Latitude': center_latitude,
        'Center Longitude': center_longitude
    }

# Example usage
if __name__ == "__main__":
    file_path = "coordinates2011.csv"  # Replace with the actual file path
    result = find_border_extremes_and_center(file_path)
    
    print("Highest Latitude:", result['Highest Latitude'])
    print("Lowest Latitude:", result['Lowest Latitude'])
    print("Highest Longitude:", result['Highest Longitude'])
    print("Lowest Longitude:", result['Lowest Longitude'])
    print("Center Latitude:", result['Center Latitude'])
    print("Center Longitude:", result['Center Longitude'])
