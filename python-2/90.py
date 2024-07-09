import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define inputs
smoothK = 3
smoothD = 3
lengthRSI = 14
lengthStoch = 14

# Calculate RSI
df['rsi1'] = talib.RSI(df['close'], timeperiod=lengthRSI)

# Calculate Stochastic RSI
df['fastk'], df['fastd'] = talib.STOCHRSI(df['rsi1'], timeperiod=lengthStoch, fastk_period=smoothK, fastd_period=smoothD, fastd_matype=0)

# Rename columns to match Pine Script plots
df = df.rename(columns={'fastk': 'Stochastic RSI-1', 'fastd': 'Stochastic RSI-2'})

# Save updated data to CSV
df.to_csv('data.csv', index=False)

