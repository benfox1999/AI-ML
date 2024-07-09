import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define MACD parameters
fast_ma_period = 12
slow_ma_period = 26
signal_period = 9

# Calculate MACD
df['macd'], _, _ = talib.MACD(df['close'], fastperiod=fast_ma_period, slowperiod=slow_ma_period, signalperiod=signal_period)

# Shift MACD for comparison
df['prev_macd'] = df['macd'].shift(1)

# Generate '4 colour MACD' signal
df['4 colour MACD'] = np.where(df['macd'] > 0, 
                                 np.where(df['macd'] > df['prev_macd'], 1, 0),  # Lime (1) or Green (0)
                                 np.where(df['macd'] < df['prev_macd'], -1, 0)) # Maroon (-1) or Red (0)

# Save the updated DataFrame to 'data.csv'
df.to_csv('data.csv', index=False)
