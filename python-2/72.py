import pandas as pd
import numpy as np
import talib

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

# Calculate the 'Price Volume Trend' (PVT) indicator
close_change = df['close'].pct_change()
df['volume_multiplied'] = close_change * df['volume']
df['Price Volume Trend'] = df['volume_multiplied'].cumsum()

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)
