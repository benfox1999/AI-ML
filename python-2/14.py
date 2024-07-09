import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Calculate Average True Range (ATR)
def calculate_atr(df, length=14, smoothing='RMA'):
    """
    Calculates the Average True Range (ATR)

    Args:
        df (pd.DataFrame): DataFrame with 'high', 'low', 'close' columns.
        length (int, optional): ATR period. Defaults to 14.
        smoothing (str, optional): Smoothing method ('RMA', 'SMA', 'EMA', 'WMA'). 
                                     Defaults to 'RMA'.

    Returns:
        pd.Series: ATR values.
    """
    atr = talib.TRANGE(df['high'], df['low'], df['close'])
    if smoothing == 'RMA':
        atr = talib.SMA(atr, timeperiod=length)
    elif smoothing == 'SMA':
        atr = talib.SMA(atr, timeperiod=length)
    elif smoothing == 'EMA':
        atr = talib.EMA(atr, timeperiod=length)
    elif smoothing == 'WMA':
        atr = talib.WMA(atr, timeperiod=length)
    return atr

# Calculate and add ATR to the DataFrame
df['Average True Range'] = calculate_atr(df, length=14, smoothing='RMA')

# Save the updated DataFrame to 'data.csv'
df.to_csv('data.csv', index=False)
