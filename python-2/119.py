import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define Williams %R calculation function
def williams_percent_r(close, length):
  max_high = close.rolling(length).max()
  min_low = close.rolling(length).min()
  return 100 * (close - max_high) / (max_high - min_low)

# Calculate Williams %R
df['Williams %R'] = williams_percent_r(df['close'], 14)

# Save updated DataFrame to CSV
df.to_csv('data.csv', index=False)
