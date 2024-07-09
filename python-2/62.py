import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define WMA calculation function
def calculate_wma(src, length):
  return talib.WMA(src, length)

# Set input parameters
length = 9 
# Assuming 'close' column for src
src = df['close'] 

# Calculate WMA
df['Moving Average Weighted'] = calculate_wma(src, length)

# Save updated data to CSV
df.to_csv('data.csv', index=False)
