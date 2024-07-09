import pandas as pd
import numpy as np
import talib

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('data.csv')

# Convert 'open_time' and 'close_time' to datetime objects
df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')

# Set 'open_time' as the DataFrame index
df = df.set_index('open_time')

# Function to calculate 24-hour rolling sum of volume
def sum24hVol(data):
    msIn24h = 24 * 60 * 60 * 1000
    return data.rolling(f'{msIn24h}ms', closed='left').sum()

# Apply volume calculation based on 'volumetype'
# Note: 'syminfo.volumetype' logic is omitted as it's specific to TradingView
# Adjust calculation based on your data source
df['expr'] = df['close'] * df['volume']  # Example assuming 'quote' volume type

# Calculate 24-hour volume
df['24H Volume'] = sum24hVol(df['expr'])

# Reset index to original state
df = df.reset_index()

# Save the updated DataFrame to 'data.csv', overwriting the original file
df.to_csv('data.csv', index=False)
