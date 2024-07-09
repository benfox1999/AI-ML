import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define Pine Script inputs
length = 20
mult = 2.0
lengthKC = 20
multKC = 1.5
useTrueRange = True

# Calculate BB
df['basis'] = talib.SMA(df['close'], timeperiod=length)
df['dev'] = multKC * talib.STDDEV(df['close'], timeperiod=length)
df['upperBB'] = df['basis'] + df['dev']
df['lowerBB'] = df['basis'] - df['dev']

# Calculate KC
df['ma'] = talib.SMA(df['close'], timeperiod=lengthKC)
df['range'] = talib.TRANGE(df['high'], df['low'], df['close']) if useTrueRange else (df['high'] - df['low'])
df['rangema'] = talib.SMA(df['range'], timeperiod=lengthKC)
df['upperKC'] = df['ma'] + df['rangema'] * multKC
df['lowerKC'] = df['ma'] - df['rangema'] * multKC

# Determine squeeze conditions
df['sqzOn'] = (df['lowerBB'] > df['lowerKC']) & (df['upperBB'] < df['upperKC'])
df['sqzOff'] = (df['lowerBB'] < df['lowerKC']) & (df['upperBB'] > df['upperKC'])
df['noSqz'] = (df['sqzOn'] == False) & (df['sqzOff'] == False)

# Calculate 'val' (linear regression)
df['val'] = talib.LINEARREG(df['close'] - ((talib.MAX(df['high'], timeperiod=lengthKC) + talib.MIN(df['low'], timeperiod=lengthKC)) / 2).rolling(window=lengthKC).mean(), timeperiod=lengthKC)

# Apply conditional coloring logic (not directly applicable to CSV output)
# bcolor logic is omitted as it's for visual plotting

# 'scolor' logic is simplified to a single column representing the combined condition
df['Squeeze Momentum Indicator [LazyBear]'] = np.where(df['noSqz'], 'blue', np.where(df['sqzOn'], 'black', 'gray'))

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)
