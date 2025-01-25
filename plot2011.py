import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
file_path = r'C:\Users\denni\Downloads\coordinates2011.csv'
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