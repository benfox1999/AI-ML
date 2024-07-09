import pandas as pd
import numpy as np
import talib

# Load CSV data, addressing mixed types and suppress warning
data = pd.read_csv('data.csv', low_memory=False, dtype={'14': str, '15': str})  

# MACD Strategy Parameters
fastLength = 12
slowLength = 26
MACDLength = 9

# Calculate MACD and Signal Line
data['MACD'] = talib.EMA(data['close'], fastLength) - talib.EMA(data['close'], slowLength)
data['aMACD'] = talib.EMA(data['MACD'], MACDLength)
data['delta'] = data['MACD'] - data['aMACD']

# Generate Trading Signals (Using bitwise & instead of 'and')
data['MACD Strategy-buy'] = np.where((data['delta'].shift(1) < 0) & (data['delta'] > 0), 1, 0)
data['MACD Strategy-sell'] = np.where((data['delta'].shift(1) > 0) & (data['delta'] < 0), -1, 0)

# Save the updated DataFrame to the CSV file
data.to_csv('data.csv', index=False)
