import pandas as pd
import numpy as np

# Avoid directly importing CROSSOVER and CROSSUNDER from talib
import talib

# Load data from CSV, handling mixed types and suppressing warning
data = pd.read_csv("data.csv", low_memory=False, dtype={'14': str, '15': str})  

# Define moving average periods
fast_length = 9
slow_length = 18

# Calculate moving averages
data['mafast'] = talib.SMA(data['close'], timeperiod=fast_length)
data['maslow'] = talib.SMA(data['close'], timeperiod=slow_length)

# Generate buy/sell signals (using numpy for crossovers)
data['MovingAvg2Line Cross-buy'] = np.where(
    (data['mafast'] > data['maslow']) & (data['mafast'].shift(1) <= data['maslow'].shift(1)), 1, 0)
data['MovingAvg2Line Cross-sell'] = np.where(
    (data['mafast'] < data['maslow']) & (data['mafast'].shift(1) >= data['maslow'].shift(1)), 1, 0)

# Save the updated DataFrame to a CSV file
data.to_csv("data.csv", index=False)
