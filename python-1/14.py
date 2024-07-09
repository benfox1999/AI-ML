import pandas as pd
import numpy as np
import talib

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

# Calculate the strategy logic
df['OutBarLE'] = np.where((df['high'] > df['high'].shift(1)) & (df['low'] < df['low'].shift(1)) & (df['close'] > df['open']), 1, 0)
df['OutBarSE'] = np.where((df['high'] > df['high'].shift(1)) & (df['low'] < df['low'].shift(1)) & (df['close'] < df['open']), 1, 0)

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)
