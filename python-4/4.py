import pandas as pd
import numpy as np
import talib

# Load data from CSV
df = pd.read_csv('data.csv')



# Option 2: Calculate an approximation for 'open' (uncomment if you want this)
# df['open'] = df['close'].shift(1)  

# Define Pine Script inputs
n1 = 10
n2 = 21
obLevel1 = 60
obLevel2 = 53
osLevel1 = -60
osLevel2 = -53

# Calculate WaveTrend indicator
df['ap'] = talib.AVGPRICE(df['open'], df['high'], df['low'], df['close'])
df['esa'] = df['ap'].ewm(span=n1, adjust=False).mean()
df['d'] = (df['ap'] - df['esa']).abs().ewm(span=n1, adjust=False).mean()
df['ci'] = (df['ap'] - df['esa']) / (0.015 * df['d'])
df['tci'] = df['ci'].ewm(span=n2, adjust=False).mean()

df['wt1'] = df['tci']
df['wt2'] = df['wt1'].rolling(window=4).mean()

# WaveTrend [LazyBear] strategy
df['WaveTrend [LazyBear]'] = np.where(df['wt1'] > df['wt2'], 1, -1)

# Save the updated DataFrame to data.csv
df.to_csv('data.csv', index=False)  # Save to a new file
