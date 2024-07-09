import pandas as pd
import numpy as np

# Load the CSV data
df = pd.read_csv('data.csv')

# Convert timestamps to datetime objects if needed
# df['open_time'] = pd.to_datetime(df['open_time'])
# df['close_time'] = pd.to_datetime(df['close_time'])

# Initialize an empty list to store source values (similar to Pine Script array)
src_vals = []

# Iterate through the DataFrame rows
for index, row in df.iterrows():
    # Simulate Pine Script's visible bar logic using a fixed window
    # Adjust window_size as needed 
    window_size = 10  
    if index >= window_size:
        src_vals.append(row['close'])  # Using 'close' as the source (src)

        # Calculate the average of the source values
        avg_src = np.mean(src_vals)

        # Add the calculated value to the DataFrame
        df.loc[index, 'Visible Average Price'] = avg_src

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False) 
