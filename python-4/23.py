import pandas as pd
import numpy as np
import talib

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

# Define the Pine Script input parameters
len = 14
upLine = 70
lowLine = 30
resCustom = '60'  # Assuming '60' represents a 60-minute timeframe
len2 = 14
resCustom2 = 'D'  # Assuming 'D' represents a daily timeframe

# Calculate the RSI values
df['up'] = talib.SMA(np.maximum(df['close'].diff(), 0), len)
df['down'] = talib.SMA(-np.minimum(df['close'].diff(), 0), len)
df['rsi'] = np.where(df['down'] == 0, 100, np.where(df['up'] == 0, 0, 100 - (100 / (1 + df['up'] / df['down']))))

# Calculate the RSI values for the second RSI
df['up2'] = talib.SMA(np.maximum(df['close'].diff(), 0), len2)
df['down2'] = talib.SMA(-np.minimum(df['close'].diff(), 0), len2)
df['rsi2'] = np.where(df['down2'] == 0, 100, np.where(df['up2'] == 0, 0, 100 - (100 / (1 + df['up2'] / df['down2']))))

# Calculate the trading signals
df['CM_Ultimate RSI MTF-buy'] = np.where((df['rsi'].shift(1) < lowLine) & (df['rsi'] > lowLine), 1, 0)
df['CM_Ultimate RSI MTF-sell'] = np.where((df['rsi'].shift(1) > upLine) & (df['rsi'] < upLine), 1, 0)

# Save the updated DataFrame to a CSV file
df.to_csv('data.csv', index=False)
