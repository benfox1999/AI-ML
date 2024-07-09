import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Inside Bar Strategy
df['InsBarLE'] = np.where((df['high'] < df['high'].shift(1)) & 
                          (df['low'] > df['low'].shift(1)) & 
                          (df['close'] > df['open']), 1, 0)

df['InsBarSE'] = np.where((df['high'] < df['high'].shift(1)) & 
                          (df['low'] > df['low'].shift(1)) & 
                          (df['close'] < df['open']), 1, 0)

# Save the updated DataFrame back to the CSV file
df.to_csv('data.csv', index=False)
