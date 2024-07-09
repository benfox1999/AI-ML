import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Settings (matching Pine Script inputs)
length = 20
mult = 2.0
atrlength = 10

# Calculate Exponential Moving Average (EMA) function
def esma(data, length):
    return data.ewm(span=length, adjust=False).mean()

# Calculate Keltner Channel bands
df['ma'] = esma(df['close'], length)
df['rangema'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=atrlength)
df['upper'] = df['ma'] + df['rangema'] * mult
df['lower'] = df['ma'] - df['rangema'] * mult

# Identify crossovers
df['crossUpper'] = (df['close'] > df['upper']) & (df['close'].shift(1) <= df['upper'].shift(1))
df['crossLower'] = (df['close'] < df['lower']) & (df['close'].shift(1) >= df['lower'].shift(1))

# Initialize buy/sell price and condition columns
df['bprice'] = 0.0
df['sprice'] = 0.0
df['crossBcond'] = False
df['crossScond'] = False

# Loop through DataFrame for strategy logic (Pine Script loop replacement)
for i in range(1, len(df)):
    df.loc[i, 'bprice'] = df['high'][i] if df['crossUpper'][i] else df['bprice'][i - 1]
    df.loc[i, 'sprice'] = df['low'][i] if df['crossLower'][i] else df['sprice'][i - 1]
    df.loc[i, 'crossBcond'] = True if df['crossUpper'][i] else df['crossBcond'][i - 1]
    df.loc[i, 'crossScond'] = True if df['crossLower'][i] else df['crossScond'][i - 1]

# Determine strategy signals
df['Keltner Channels Strategy-buy'] = (df['crossUpper']) & (df['crossBcond'])
df['Keltner Channels Strategy-sell'] = (df['crossLower']) & (df['crossScond'])

# Save the updated DataFrame to CSV
df.to_csv('data.csv', index=False) 
