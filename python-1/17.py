import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define Pivot function (Pine Script's pivothigh/pivotlow equivalent)
def pivot(df, leftBars, rightBars, high_low):
    pivots = np.nan * np.ones(len(df))
    for i in range(leftBars + rightBars, len(df)):
        window = df[i - (leftBars + rightBars):i + 1]
        if high_low == 'high':
            pivot_val = window['high'].max() if len(window) > 0 else np.nan
        else:
            pivot_val = window['low'].min() if len(window) > 0 else np.nan
        if (high_low == 'high' and window['high'].iloc[-rightBars-1] == pivot_val) or (high_low == 'low' and window['low'].iloc[-rightBars-1] == pivot_val):
            pivots[i] = pivot_val
    return pivots

# Set input parameters
leftBars = 4
rightBars = 2

# Calculate swing high and low
df['swh'] = pivot(df, leftBars, rightBars, 'high')
df['swl'] = pivot(df, leftBars, rightBars, 'low')

# Initialize trading signals
df['PivRevLE'] = pd.Series(False, index=df.index) 
df['PivRevSE'] = pd.Series(False, index=df.index)

# Generate trading signals using vectorized operations
df['hprice'] = df['swh'].ffill()  # Forward fill for price comparisons
df['lprice'] = df['swl'].ffill()

df['PivRevLE'] = (
    (df['swh'].notnull())  
    & (df['high'] <= df['hprice'])  
    & (df['PivRevLE'].shift(1) | (df['high'] <= df['hprice'].shift(1)))  
)

df['PivRevSE'] = (
    (df['swl'].notnull())
    & (df['low'] >= df['lprice'])
    & (df['PivRevSE'].shift(1) | (df['low'] >= df['lprice'].shift(1)))
)

# Save the updated DataFrame to CSV
df.to_csv('data.csv', index=False)
