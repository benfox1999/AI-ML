import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Convert timestamps if needed (assuming they are in standard format)
# df['open_time'] = pd.to_datetime(df['open_time'])
# df['close_time'] = pd.to_datetime(df['close_time'])

def up_and_down_volume(df):
    df['isBuyVolume'] = np.where(
        (df['close'] > df['open']) |
        (df['close'] > df['close'].shift(1)), 
        True, 
        False
    )

    df['volume_delta'] = np.where(
        df['isBuyVolume'], 
        df['volume'], 
        -df['volume']
    )
    return df['volume_delta'].values

# Function to simulate request.security_lower_tf 
# (simplified, assuming default 'lowerTimeframe' for now)
def get_lower_timeframe_data(df):
    return up_and_down_volume(df)

def get_high_low(arr):
    cum_volume = np.cumsum(arr)
    max_volume = np.maximum.accumulate(cum_volume)
    min_volume = np.minimum.accumulate(cum_volume)
    return max_volume[-1], min_volume[-1], cum_volume[-1]

# Main calculation loop
volume_delta = get_lower_timeframe_data(df)
max_volume, min_volume, last_volume = get_high_low(volume_delta)

df['Volume Delta'] = last_volume

# Save the updated DataFrame to the CSV
df.to_csv('data.csv', index=False) 
