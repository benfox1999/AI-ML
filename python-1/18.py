import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Calculate highest high and lowest low
length = 20
df['hh'] = df['high'].rolling(window=length).max()
df['ll'] = df['low'].rolling(window=length).min()

# Initialize strategy columns
df['PChLE'] = 0 
df['PChSE'] = 0

# Generate buy/sell signals using .loc for explicit assignment
df.loc[length:, 'PChLE'] = np.where(
    df['close'][length:] > df['hh'][length:], 1, 0
) 

df.loc[length:, 'PChSE'] = np.where(
    df['close'][length:] < df['ll'][length:], 1, 0
)

# Save updated DataFrame to CSV
df.to_csv('data.csv', index=False)
