import pandas as pd
import numpy as np
import talib

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('data.csv')

# Define the VWMA function
def vwma(src, length):
    """
    Calculates the Volume Weighted Moving Average (VWMA).
    """
    typical_price = (df['close'] + df['high'] + df['low']) / 3
    pv = typical_price * df['volume']
    vwma = talib.SMA(pv, timeperiod=length) / talib.SMA(df['volume'], timeperiod=length)
    return vwma

# Calculate the VWMA
df['VWMA'] = vwma(df['close'], 20)

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)
