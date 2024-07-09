import pandas as pd
import numpy as np


# Load CSV data with type conversion for specific columns
data = pd.read_csv('data.csv', dtype={'14': float, '15': float, '354': float}, low_memory=False)


# Define the Donchian Channel length
length = 20

# Calculate the Donchian Channel values directly
data['Donchian Channels-1'] = (
    (data['high'].rolling(window=length).max() + data['low'].rolling(window=length).min()) / 2
)
data['Donchian Channels-2'] = data['high'].rolling(window=length).max()
data['Donchian Channels-3'] = data['low'].rolling(window=length).min()

# Handle NaN values (optional)
data[['Donchian Channels-1', 'Donchian Channels-2', 'Donchian Channels-3']] = data[
    ['Donchian Channels-1', 'Donchian Channels-2', 'Donchian Channels-3']
].bfill()

# Save the updated DataFrame back to the CSV file
data.to_csv('data.csv', index=False)
