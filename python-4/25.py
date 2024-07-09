import pandas as pd
import numpy as np
import talib

# Load data from CSV
df = pd.read_csv('data.csv')

# Define inputs
n1 = 10  # Channel Length
n2 = 21  # Average Length
obLevel1 = 60  # Over Bought Level 1
obLevel2 = 53  # Over Bought Level 2
osLevel1 = -60  # Over Sold Level 1
osLevel2 = -53  # Over Sold Level 2

# Calculate Average Price
df['ap'] = (df['high'] + df['low'] + df['close']) / 3

# Calculate EMA of Average Price
df['esa'] = talib.EMA(df['ap'], timeperiod=n1)

# Calculate the absolute difference between Average Price and its EMA
df['abs_diff'] = abs(df['ap'] - df['esa'])

# Calculate EMA of the absolute difference
df['d'] = talib.EMA(df['abs_diff'], timeperiod=n1)

# Calculate the WaveTrend indicator components
df['ci'] = (df['ap'] - df['esa']) / (0.015 * df['d'])
df['tci'] = talib.EMA(df['ci'], timeperiod=n2)

# Calculate WaveTrend with Crosses
df['wt1'] = df['tci']
df['wt2'] = talib.SMA(df['wt1'], timeperiod=4)

# Identify buy and sell signals
df['WaveTrend with Crosses [LazyBear]'] = np.where(df['wt1'] > df['wt2'], 1, 0)

# Save the updated DataFrame to a CSV file
df.to_csv('data.csv', index=False)
