
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file containing city border coordinates
csv_file = 'coordinates1964.csv'  # Make sure to update the path if necessary
coordinates_df = pd.read_csv(csv_file)

# Plotting the coordinates on a grid
plt.figure(figsize=(8, 8))
plt.scatter(coordinates_df['Longitude'], coordinates_df['Latitude'], color='blue', marker='o', label='City Border')

# Adding grid lines
plt.grid(True)

# Setting labels and title
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('City Border Visualization on Grid')

# Display the plot
plt.legend()
plt.show()
