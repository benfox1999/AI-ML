import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Convert 'open_time' and 'close_time' to datetime objects if needed
df['open_time'] = pd.to_datetime(df['open_time'])
df['close_time'] = pd.to_datetime(df['close_time'])

# Define input parameters
leftBars = 15
rightBars = 15
volumeThresh = 20

# Function to calculate Pivot Points manually
def calculate_pivot_points(df, leftBars, rightBars):
    pivot_high = (df['high'].shift(1).rolling(window=leftBars+rightBars+1).max()).shift(-rightBars)
    pivot_low = (df['low'].shift(1).rolling(window=leftBars+rightBars+1).min()).shift(-rightBars)

    return pivot_high, pivot_low

# Calculate Pivot Points
df['highUsePivot'], df['lowUsePivot'] = calculate_pivot_points(df, leftBars, rightBars)

# Fill NaN values with previous values to ensure plotting continuity
df['highUsePivot'].fillna(method='ffill', inplace=True)
df['lowUsePivot'].fillna(method='ffill', inplace=True)

# Calculate Volume Oscillator
df['short_ema'] = talib.EMA(df['volume'], timeperiod=5)
df['long_ema'] = talib.EMA(df['volume'], timeperiod=10)
df['osc'] = 100 * (df['short_ema'] - df['long_ema']) / df['long_ema']

# Identify Break Conditions 
df[' Support and Resistance Levels with Breaks-buy'] = (
    (df['close'] < df['lowUsePivot']) & 
    (df['open'] - df['close'] >= df['high'] - df['open']) & 
    (df['osc'] > volumeThresh)
)

df[' Support and Resistance Levels with Breaks-sell'] = (
    (df['close'] > df['highUsePivot']) & 
    (df['open'] - df['low'] <= df['close'] - df['open']) & 
    (df['osc'] > volumeThresh)
)

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)
