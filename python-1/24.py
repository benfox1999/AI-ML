import pandas as pd
import numpy as np
import talib

# Load data from CSV
data = pd.read_csv('data.csv')

# Define function to calculate Average True Range (ATR)
def atr(df, length):
    return talib.ATR(df['high'], df['low'], df['close'], timeperiod=length)

# Input parameters
length = 5
numATRs = 0.75

# Calculate ATR
data['ATR'] = atr(data, length)

# Calculate entry signals
data['VltClsLE'] = np.where((data['ATR'].shift(1) * numATRs + data['close'].shift(1) < data['close']) & (data['ATR'].notna()), 1, 0)
data['VltClsSE'] = np.where((data['close'].shift(1) - data['ATR'].shift(1) * numATRs > data['close']) & (data['ATR'].notna()), 1, 0)

# Save the updated DataFrame to 'data.csv'
data.to_csv('data.csv', index=False)
