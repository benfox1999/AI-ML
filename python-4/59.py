import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Convert 'open_time' and 'close_time' to datetime objects if needed
df['open_time'] = pd.to_datetime(df['open_time'])
df['close_time'] = pd.to_datetime(df['close_time'])

# Define function to calculate MACD
def calculate_macd(df, res, fast_length, slow_length, signal_length, sma_source, sma_signal):
    # Requesting data from a different timeframe is not supported, using current timeframe
    # Assuming 'res' is not used further
    if sma_source == "SMA":
        fast_ma = df['close'].rolling(window=fast_length).mean()
        slow_ma = df['close'].rolling(window=slow_length).mean()
    else:  # sma_source == "EMA"
        fast_ma = talib.EMA(df['close'], timeperiod=fast_length)
        slow_ma = talib.EMA(df['close'], timeperiod=slow_length)

    macd = fast_ma - slow_ma
    
    if sma_signal == "SMA":
        signal = macd.rolling(window=signal_length).mean()
    else: #sma_signal == "EMA"
        signal = talib.EMA(macd, timeperiod=signal_length)

    hist = macd - signal
    return macd, signal, hist

# Set indicator parameters
res = None  # Timeframe is not used in calculation
fast_length = 12
slow_length = 26
signal_length = 9
sma_source = "EMA" 
sma_signal = "EMA"

# Calculate MACD
df['macd'], df['signal'], df['hist'] = calculate_macd(df, res, fast_length, slow_length, signal_length, sma_source, sma_signal)

# Determine cross conditions
df['trend_up'] = df['macd'] > df['signal']
df['trend_dn'] = df['macd'] < df['signal']
df['cross_UP'] = (df['signal'].shift(1) >= df['macd'].shift(1)) & (df['signal'] < df['macd'])
df['cross_DN'] = (df['signal'].shift(1) <= df['macd'].shift(1)) & (df['signal'] > df['macd'])

# Add buy/sell signals to DataFrame (example - replace with actual logic)
df['_CM_MacD_Ult_MTF_V2.1'] = np.where(df['cross_UP'], 1, 0) 

# Save updated data to CSV
df.to_csv('data.csv', index=False)

