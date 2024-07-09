import pandas as pd
import numpy as np
import talib

# Load the CSV data
df = pd.read_csv('data.csv')

# Define the Stochastic parameters
length = 14
overbought = 80
oversold = 20
smooth_k = 3
smooth_d = 3

# Calculate the Stochastic Oscillator
df['k'] = talib.SMA(talib.STOCH(df['high'], df['low'], df['close'], fastk_period=length)[0], smooth_k)
df['d'] = talib.SMA(df['k'], smooth_d)

# Identify buy and sell signals
df['StochLE'] = np.where((df['k'].shift(1) < df['d'].shift(1)) & (df['k'] > df['d']) & (df['k'] < oversold), 1, 0)
df['StochSE'] = np.where((df['k'].shift(1) > df['d'].shift(1)) & (df['k'] < df['d']) & (df['k'] > overbought), 1, 0)

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)
