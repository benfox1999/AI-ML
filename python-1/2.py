import pandas as pd
import numpy as np
import talib

# Load data from CSV
df = pd.read_csv('data.csv')

# Define strategy parameters
length = 20
mult = 2.0
direction = 0  # 0: all, -1: short only, 1: long only

# Calculate Bollinger Bands
df['basis'] = talib.SMA(df['close'], timeperiod=length)
df['dev'] = mult * talib.STDDEV(df['close'], timeperiod=length)
df['upper'] = df['basis'] + df['dev']
df['lower'] = df['basis'] - df['dev']

# Initialize buy/sell signals (using pd.Series to avoid the SettingWithCopyWarning)
df['Bollinger Bands Strategy directed-buy'] = pd.Series(np.nan, index=df.index)
df['Bollinger Bands Strategy directed-sell'] = pd.Series(np.nan, index=df.index)

# Generate trading signals (using .loc for explicit index-based assignment)
for i in range(length, len(df)):
    if direction == 0 or direction == 1:
        if df['close'][i] > df['lower'][i] and df['close'][i - 1] <= df['lower'][i - 1]:
            df.loc[i, 'Bollinger Bands Strategy directed-buy'] = 1

    if direction == 0 or direction == -1:
        if df['close'][i] < df['upper'][i] and df['close'][i - 1] >= df['upper'][i - 1]:
            df.loc[i, 'Bollinger Bands Strategy directed-sell'] = 1

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)
