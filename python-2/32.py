import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Convert timestamps to datetime objects
df['open_time'] = pd.to_datetime(df['open_time'])
df['close_time'] = pd.to_datetime(df['close_time'])

def calculate_cvd(df):
    # Calculate up and down volume
    df['up_volume'] = np.where(df['close'] > df['open'], df['volume'], 0)
    df['down_volume'] = np.where(df['close'] < df['open'], df['volume'], 0)

    # Calculate cumulative volume delta
    df['Cumulative Volume Delta'] = (df['up_volume'] - df['down_volume']).cumsum()
    
    return df

# Apply calculations
df = calculate_cvd(df)

# Save the updated DataFrame back to data.csv
df.to_csv('data.csv', index=False)
