import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv("data.csv")

# MACD Inputs (using default values from Pine Script)
fast_length = 12
slow_length = 26
signal_length = 9

# Calculate MACD
df['MACD'] = talib.EMA(df['close'], timeperiod=fast_length) - talib.EMA(df['close'], timeperiod=slow_length)
df['Signal'] = talib.EMA(df['MACD'], timeperiod=signal_length)
df['Histogram'] = df['MACD'] - df['Signal']

# Save updated DataFrame to CSV
df.to_csv("data.csv", index=False)
