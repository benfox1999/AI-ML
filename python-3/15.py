import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Convert timestamp columns to datetime objects if needed
df['open_time'] = pd.to_datetime(df['open_time'])
df['close_time'] = pd.to_datetime(df['close_time'])

def calculate_bias(df, tf):
    """
    Calculates the bias based on the given timeframe.

    Args:
        df (pd.DataFrame): DataFrame with OHLC data.
        tf (str): Timeframe ('D' for daily, 'W' for weekly).

    Returns:
        pd.DataFrame: DataFrame with 'bias' column added.
    """
    df['new_' + tf] = (df['open_time'].dt.to_period(tf) != df['open_time'].dt.to_period(tf).shift(1)).astype(int)

    n = {
        'ph': np.nan, 
        'pl': np.nan, 
        'ch': df['high'].iloc[0], 
        'cl': df['low'].iloc[0], 
        'co': df['open'].iloc[0], 
        'p_up': True, 
        'bias': 0
    }

    bias_list = []
    for i in range(len(df)):
        if df['new_' + tf][i] == 1:
            if not np.isnan(n['ch']):
                if i>0: # check if i is greater than 0 before we compare previous row with current
                    if df['close'][i - 1] > n['ph']:
                        n['bias'] = 1
                    elif df['close'][i-1] < n['pl']:
                        n['bias'] = -1
                    elif df['close'][i-1] < n['ph'] and df['close'][i-1] > n['pl'] and n['ch'] > n['ph'] and n['cl'] > n['pl']:
                        n['bias'] = -1
                    elif df['close'][i-1] > n['pl'] and df['close'][i-1] < n['ph'] and n['ch'] < n['ph'] and n['cl'] < n['pl']:
                        n['bias'] = 1
                    elif n['ch'] <= n['ph'] and n['cl'] >= n['pl']:
                        n['bias'] = 1 if n['p_up'] else -1
                    else:
                        n['bias'] = 0

                    if df['close'][i-1] >= n['co']:
                        n['p_up'] = True
                    else:
                        n['p_up'] = False

                n['ph'] = n['ch']
                n['pl'] = n['cl']

            n['ch'] = df['high'][i]
            n['cl'] = df['low'][i]
            n['co'] = df['open'][i]
        else:
            n['ch'] = max(df['high'][i], n['ch'])
            n['cl'] = min(df['low'][i], n['cl'])

        bias_list.append(n['bias'])

    df['bias_' + tf] = bias_list
    return df

# Calculate daily and weekly bias
df = calculate_bias(df.copy(), 'D')
df = calculate_bias(df.copy(), 'W')

# Save the updated DataFrame to a CSV file
df.to_csv('data.csv', index=False)

