import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
file_path = r'C:\Users\denni\Downloads\coordinates2005.csv'
data = pd.read_csv(file_path)

# Extract columns
col1 = data.iloc[:, 0]  # First column
col2 = data.iloc[:, 1]  # Second column

# Plot the data
plt.plot(col1, col2)
plt.xlabel('Column 1')
plt.ylabel('Column 2')
plt.title('Plot of CSV Data')
plt.grid(True)
plt.show()

# Load the CSV and skip the non-numeric header
data = pd.read_csv('your_file.csv', header=0)  # Assumes the first row is the header

# If there's extra non-numeric data elsewhere, you can clean it
data = data.apply(pd.to_numeric, errors='coerce')  # Convert to numbers, replace non-numeric with NaN
data = data.dropna()  # Drop rows with NaN values

# Extract x and y columns (replace 'x_column' and 'y_column' with your actual column names)
x = data['x_column'].values
y = data['y_column'].values