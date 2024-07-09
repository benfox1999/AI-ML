import pandas as pd
import numpy as np
import talib

# Load the CSV file into a Pandas DataFrame
data = pd.read_csv('data.csv')

# Calculate RSI
data['up'] = data['close'].diff().apply(lambda x: max(x, 0)).rolling(window=2).mean()
data['down'] = -data['close'].diff().apply(lambda x: min(x, 0)).rolling(window=2).mean()
data['rsi'] = np.where(data['down'] == 0, 100, np.where(data['up'] == 0, 0, 100 - (100 / (1 + data['up'] / data['down']))))

# Calculate moving averages
data['ma5'] = talib.SMA(data['close'], timeperiod=5)
data['ma200'] = talib.SMA(data['close'], timeperiod=200)

# Generate trading signals
data['_CM_RSI_2_Strat_Low'] = np.where((data['close'] > data['ma200']) & (data['close'] < data['ma5']) & (data['rsi'] < 10), 1, 0)

# Save the DataFrame back to a CSV file
data.to_csv('data.csv', index=False)
