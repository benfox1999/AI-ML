import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Calculate SMMA (Smoothed Moving Average)
def calculate_smma(src, length):
    smma = np.zeros_like(src, dtype=float)
    sma = talib.SMA(src, length)
    for i in range(length, len(src)):
        smma[i] = (smma[i - 1] * (length - 1) + src[i]) / length
    smma[:length] = sma[:length]  # Fill initial values with SMA
    return smma

df['21 SMMA'] = calculate_smma(df['close'], 21)
df['50 SMMA'] = calculate_smma(df['close'], 50)
df['100 SMMA'] = calculate_smma(df['close'], 100)
df['200 SMMA'] = calculate_smma(df['close'], 200)

# Calculate EMA (Exponential Moving Average)
df['EMA(2)'] = talib.EMA(df['close'], timeperiod=2)

# Trend Fill (Determine buy/sell signals based on EMA and SMMA crossover)
df['Trend Fill-buy'] = np.where((df['EMA(2)'] > df['200 SMMA']), 1, 0)
df['Trend Fill-sell'] = np.where((df['EMA(2)'] < df['200 SMMA']), 1, 0)

# 3 Line Strike
df['3 Line Strike-buy'] = np.where(
    (df['close'].shift(3) < df['open'].shift(3)) &
    (df['close'].shift(2) < df['open'].shift(2)) &
    (df['close'].shift(1) < df['open'].shift(1)) &
    (df['close'] > df['open'].shift(1)), 1, 0)

df['3 Line Strike-sell'] = np.where(
    (df['close'].shift(3) > df['open'].shift(3)) &
    (df['close'].shift(2) > df['open'].shift(2)) &
    (df['close'].shift(1) > df['open'].shift(1)) &
    (df['close'] < df['open'].shift(1)), 1, 0)

# Big A$$ Candles (Engulfing Candles)
df['Big A$$ Candles-buy'] = np.where(
    (df['open'] <= df['close'].shift(1)) &
    (df['open'] < df['open'].shift(1)) &
    (df['close'] > df['open'].shift(1)), 1, 0)

df['Big A$$ Candles-sell'] = np.where(
    (df['open'] >= df['close'].shift(1)) &
    (df['open'] > df['open'].shift(1)) &
    (df['close'] < df['open'].shift(1)), 1, 0)

# Save the updated DataFrame to a CSV file
df.to_csv('data.csv', index=False)
