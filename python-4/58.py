import pandas as pd
import numpy as np
import talib

# Load data from CSV
df = pd.read_csv('data.csv')

def calculate_rsi(series, length):
    up = np.maximum(series.diff(), 0)
    down = -np.minimum(series.diff(), 0)
    ma_up = talib.SMA(up, length)
    ma_down = talib.SMA(down, length)
    rs = ma_up / ma_down
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Calculate RSI values
df['rsi_fast'] = calculate_rsi(df['close'], 5)
df['rsi_slow'] = calculate_rsi(df['close'], 14)

# Calculate divergence
df['RSI Divergence'] = df['rsi_fast'] - df['rsi_slow']

# Save the updated DataFrame to data.csv
df.to_csv('data.csv', index=False)
