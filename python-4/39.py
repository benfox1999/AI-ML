import pandas as pd
import numpy as np
import talib

# Load data from CSV
df = pd.read_csv('data.csv')

# Define Pine Script inputs
rsi_length = 20
ema_length = 10

# Calculate RSI
df['change'] = df['close'].diff()
df['gain'] = np.where(df['change'] > 0, df['change'], 0)
df['loss'] = np.where(df['change'] < 0, -df['change'], 0)
df['avg_gain'] = df['gain'].rolling(rsi_length).mean()
df['avg_loss'] = df['loss'].rolling(rsi_length).mean()
df['rs'] = df['avg_gain'] / df['avg_loss']
df['rsi'] = 100 - (100 / (1 + df['rs']))

# Calculate EMA of RSI
df['ema_rsi'] = talib.EMA(df['rsi'], timeperiod=ema_length)

# No buy/sell signals in this strategy, so just add the indicator values
df['CM_RSI_EMA'] = df['ema_rsi']

# Save the updated DataFrame to CSV
df.to_csv('data.csv', index=False)
