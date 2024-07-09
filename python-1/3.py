import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Bollinger Bands calculation
length = 20
mult = 2.0
df['basis'] = talib.SMA(df['close'], timeperiod=length)
df['dev'] = mult * talib.STDDEV(df['close'], timeperiod=length)
df['upper'] = df['basis'] + df['dev']
df['lower'] = df['basis'] - df['dev']

# Generate buy/sell signals
df['Bollinger Bands Strategy-buy'] = ((df['close'] > df['lower']) & (df['close'].shift(1) <= df['lower'].shift(1))).astype(int)
df['Bollinger Bands Strategy-sell'] = ((df['close'] < df['upper']) & (df['close'].shift(1) >= df['upper'].shift(1))).astype(int)

# Save the updated DataFrame to 'data.csv'
df.to_csv('data.csv', index=False)
