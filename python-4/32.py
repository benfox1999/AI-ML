import pandas as pd
import numpy as np
import talib

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

# Define the Pine Script input parameters
periods = 5
threshold = 0.0
use_wicks = False

# Calculate the absolute percent move from potential OB to last candle
df['absmove'] = (abs(df['close'].shift(periods + 1) - df['close'].shift(1)) / df['close'].shift(periods + 1)) * 100

# Identify "Relevant move"
df['relmove'] = df['absmove'] >= threshold

# Bullish Order Block Identification
df['bullishOB'] = (df['close'].shift(periods + 1) < df['open'].shift(periods + 1))

# Determine the color of subsequent candles
df['upcandles'] = 0
for i in range(1, periods + 1):
    df['upcandles'] += np.where(df['close'].shift(i) > df['open'].shift(i), 1, 0)

# Identify Bullish Order Blocks
df['Order Block Finder-buy'] = (df['bullishOB']) & (df['upcandles'] == periods) & (df['relmove'])

# Bearish Order Block Identification
df['bearishOB'] = (df['close'].shift(periods + 1) > df['open'].shift(periods + 1))

# Determine the color of subsequent candles
df['downcandles'] = 0
for i in range(1, periods + 1):
    df['downcandles'] += np.where(df['close'].shift(i) < df['open'].shift(i), 1, 0)

# Identify Bearish Order Blocks
df['Order Block Finder-sell'] = (df['bearishOB']) & (df['downcandles'] == periods) & (df['relmove'])

# Save the updated DataFrame to a CSV file
df.to_csv('data.csv', index=False)
