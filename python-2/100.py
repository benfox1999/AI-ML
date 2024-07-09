import pandas as pd
import numpy as np
import talib

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

def up_down_volume(df):
    """
    Calculates up and down volume based on price and volume data.

    Args:
        df (pd.DataFrame): DataFrame with 'open', 'close', and 'volume' columns.

    Returns:
        tuple: A tuple containing two Pandas Series representing up volume and down volume.
    """

    # Initialize up volume and down volume arrays
    up_volume = np.zeros_like(df['volume'])
    down_volume = np.zeros_like(df['volume'])

    # Calculate up and down volume based on price change and previous close
    for i in range(1, len(df)):
        if df['close'][i] > df['open'][i]:
            up_volume[i] += df['volume'][i]
        elif df['close'][i] < df['open'][i]:
            down_volume[i] -= df['volume'][i]

        if df['close'][i] >= df['close'][i - 1]:
            up_volume[i] += df['volume'][i]
        elif df['close'][i] < df['close'][i - 1]:
            down_volume[i] -= df['volume'][i]

    return up_volume, down_volume

# Calculate up and down volume using the function
df['Up Volume'], df['Down Volume'] = up_down_volume(df)

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)
