import pandas as pd
import os

# Reload the CSV file since the previous session state was reset
file_path =  os.path.dirname(os.path.abspath(__file__))+'/'+'Truth_data.csv'
data = pd.read_csv(file_path)

# Remove rows where any column has the values 14204, 90012, or 70113
filtered_data = data[~data.isin([14204, 90012, 70113,85147,77008,14213,10013]).any(axis=1)]

# Save the updated filtered data to a new CSV file

filtered_data.to_csv(file_path, index=False)

