import pandas as pd
import numpy as np
import talib

# Load data from CSV
data = pd.read_csv('data.csv')

# Calculate signals
data['BarUpDn Strategy-buy'] = np.where((data['close'] > data['open']) & (data['open'] > data['close'].shift(1)), 1, 0)
data['BarUpDn Strategy-sell'] = np.where((data['close'] < data['open']) & (data['open'] < data['close'].shift(1)), -1, 0)

# Save the updated DataFrame to a CSV file
data.to_csv('data.csv', index=False) 
