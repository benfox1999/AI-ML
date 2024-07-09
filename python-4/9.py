import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Convert timestamp to datetime objects if needed
df['open_time'] = pd.to_datetime(df['open_time'])

# RSI Calculation
def calculate_rsi(df, period):
    delta = df['close'].diff()
    gain = np.where(delta >= 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

df['RSI'] = calculate_rsi(df, 6)

# Bollinger Bands Calculation
def calculate_bollinger_bands(df, period, std_dev):
    bb_basis = df['close'].rolling(window=period).mean()
    bb_std = df['close'].rolling(window=period).std()
    bb_upper = bb_basis + std_dev * bb_std
    bb_lower = bb_basis - std_dev * bb_std
    return bb_basis, bb_upper, bb_lower

df['BB_Basis'], df['BB_Upper'], df['BB_Lower'] = calculate_bollinger_bands(df, 200, 2)

# Trading Strategy
df['RSI_BB_L'] = np.where(
    (df['RSI'].shift(1) <= 50) & (df['RSI'] > 50) & 
    (df['close'].shift(1) < df['BB_Lower'].shift(1)) & (df['close'] > df['BB_Lower']), 1, 0)

df['RSI_BB_S'] = np.where(
    (df['RSI'].shift(1) >= 50) & (df['RSI'] < 50) & 
    (df['close'].shift(1) > df['BB_Upper'].shift(1)) & (df['close'] < df['BB_Upper']), 1, 0)

# Save to CSV
df.to_csv('data.csv', index=False)
