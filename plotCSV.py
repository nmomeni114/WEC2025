import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def plotCSV(file):
    current_dir = Path(__file__).parent
    csv_file = current_dir / file
    data = pd.read_csv(csv_file)

    col1 = data.iloc[:, 0]
    col2 = data.iloc[:, 1]

    plt.plot(col1, col2)
    plt.xlabel('Column 1')
    plt.ylabel('Column 2')
    plt.title('Plot of CSV Data')
    plt.grid(True)
    plt.show()

    return