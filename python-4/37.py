import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define EMA calculation function (Pine Script's ema)
def ema(data, length):
    return talib.EMA(data, length)

# Define strategy parameters
length = 20  # Default length, adjust as needed

# Calculate EMA
df['EMA'] = ema(df['close'], length)

# Calculate highest high and lowest low of the last 8 periods
df['last8h'] = df['close'].rolling(window=8).max()
df['lastl8'] = df['close'].rolling(window=8).min()

# Determine buy/sell signals
df['Tony\'s EMA Scalper - Buy / Sell-buy'] = np.where((df['close'].shift(1) < df['EMA']) & (df['close'] > df['EMA']), 1, 0)
df['Tony\'s EMA Scalper - Buy / Sell-sell'] = np.where((df['close'].shift(1) > df['EMA']) & (df['close'] < df['EMA']), 1, 0)

# Save the DataFrame with calculated columns back to 'data.csv'
df.to_csv('data.csv', index=False)
