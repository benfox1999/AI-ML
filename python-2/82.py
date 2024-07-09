import pandas as pd
import numpy as np

# Load CSV data and parse dates
df = pd.read_csv('data.csv', parse_dates=['open_time'])

# Calculate 'hlc3'
df['hlc3'] = (df['high'] + df['low'] + df['close']) / 3

# Function to calculate pivot levels for different timeframes
def get_pivot(df, timeframe):
    # Set 'open_time' as the index
    df = df.set_index('open_time')

    if timeframe == '4H':
        df_resampled = df.resample('4H').agg({'high': 'max', 'low': 'min', 'close': 'last'})
    elif timeframe == 'D':
        df_resampled = df.resample('D').agg({'high': 'max', 'low': 'min', 'close': 'last'})
    elif timeframe == 'W':
        df_resampled = df.resample('W').agg({'high': 'max', 'low': 'min', 'close': 'last'})
    elif timeframe == 'M':
        df_resampled = df.resample('M').agg({'high': 'max', 'low': 'min', 'close': 'last'})
    
    # Calculate pivot
    pivot = (df_resampled['high'].shift(1) + df_resampled['low'].shift(1) + df_resampled['close'].shift(1)) / 3

    # Reindex to match original DataFrame
    return pivot.reindex(df.index).ffill() 

# Calculate pivot levels
df['4H Pivot'] = get_pivot(df.copy(), '4H') 
df['Daily Pivot'] = get_pivot(df.copy(), 'D')
df['Weekly Pivot'] = get_pivot(df.copy(), 'W')
df['Monthly Pivot'] = get_pivot(df.copy(), 'M')

# Reset the index to bring back 'open_time' as a column
df = df.reset_index()

# Save updated data to CSV
df.to_csv('data.csv', index=False)
