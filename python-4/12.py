import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define inputs
length = 200
mult = 3.0

# Calculate VWMA (Volume Weighted Moving Average)
# Note: There is no direct equivalent of vwma in talib, so we implement it manually
df['vwma'] = (df['close'] * df['volume']).rolling(window=length).sum() / df['volume'].rolling(window=length).sum()

# Calculate standard deviation
df['stddev'] = df['close'].rolling(window=length).std()

# Calculate Fibonacci Bollinger Bands
df['upper_1'] = df['vwma'] + (0.236 * mult * df['stddev'])
df['upper_2'] = df['vwma'] + (0.382 * mult * df['stddev'])
df['upper_3'] = df['vwma'] + (0.5 * mult * df['stddev'])
df['upper_4'] = df['vwma'] + (0.618 * mult * df['stddev'])
df['upper_5'] = df['vwma'] + (0.764 * mult * df['stddev'])
df['upper_6'] = df['vwma'] + (1 * mult * df['stddev'])
df['lower_1'] = df['vwma'] - (0.236 * mult * df['stddev'])
df['lower_2'] = df['vwma'] - (0.382 * mult * df['stddev'])
df['lower_3'] = df['vwma'] - (0.5 * mult * df['stddev'])
df['lower_4'] = df['vwma'] - (0.618 * mult * df['stddev'])
df['lower_5'] = df['vwma'] - (0.764 * mult * df['stddev'])
df['lower_6'] = df['vwma'] - (1 * mult * df['stddev'])

# Save the updated DataFrame to 'data.csv'
df.to_csv('data.csv', index=False)
