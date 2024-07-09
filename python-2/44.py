import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define HMA function
def calculate_hma(src, length):
  hma = talib.WMA(2 * talib.WMA(src, length // 2) - talib.WMA(src, length), int(np.floor(np.sqrt(length))))
  return hma

# Calculate HMA
df['Hull Moving Average'] = calculate_hma(df['close'], length=9)

# Save updated DataFrame to CSV
df.to_csv('data.csv', index=False)
