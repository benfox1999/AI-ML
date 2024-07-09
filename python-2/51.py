import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv', dtype={'14': float, '15': float, '354': float}, low_memory=False)

# Define MA lengths
shortlen = 9
longlen = 21

# Calculate SMAs (convert to numeric in case of non-numeric values)
df['close'] = pd.to_numeric(df['close'], errors='coerce')
df['Short MA'] = talib.SMA(df['close'], timeperiod=shortlen)
df['Long MA'] = talib.SMA(df['close'], timeperiod=longlen)

# Function to detect crossovers (replaces talib.CROSS)
def detect_crossover(short_ma, long_ma):
    short_above_long = short_ma > long_ma
    return short_above_long & (~short_above_long).shift(1)

# Identify crossovers using the custom function
df['Cross'] = np.where(
    detect_crossover(df['Short MA'], df['Long MA']), df['Short MA'], np.nan
)

# Save the updated DataFrame to 'data.csv'
df.to_csv('data.csv', index=False)

