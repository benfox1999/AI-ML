import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Calculate CCI
length = 20
df['hlc3'] = (df['high'] + df['low'] + df['close']) / 3
df['ma'] = talib.SMA(df['hlc3'], timeperiod=length)
df['CCI'] = (df['hlc3'] - df['ma']) / (0.015 * df['hlc3'].rolling(length).std(ddof=0))

# Define smoothing function
def ma(source, length, type):
    if type == "SMA":
        return talib.SMA(source, timeperiod=length)
    elif type == "EMA":
        return talib.EMA(source, timeperiod=length)
    elif type == "SMMA (RMA)":
        return talib.SMA(source, timeperiod=length)  # RMA is the same as SMMA
    elif type == "WMA":
        return talib.WMA(source, timeperiod=length)
    elif type == "VWMA":
        return talib.VWMA(source, timeperiod=length)

# Calculate smoothing line
smoothing_length = 5
smoothing_type = "SMA" 
df['Smoothing Line'] = ma(df['CCI'], smoothing_length, smoothing_type)

# Save to CSV
df.to_csv('data.csv', index=False)
