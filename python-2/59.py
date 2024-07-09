import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Input parameters (mimicking Pine Script inputs)
len_ema = 9  # Length for EMA
offset_ema = 0  # Offset for EMA
type_ma = "SMA"  # Method for smoothing line
smoothing_length = 5  # Length for smoothing line
offset_smoothing = 0  # Offset for smoothing line

# Calculate EMA (Moving Average Exponential)
df['Moving Average Exponential'] = talib.EMA(df['close'], timeperiod=len_ema)

# Calculate smoothing line based on selected method
if type_ma == "SMA":
    df['Smoothing Line'] = talib.SMA(df['Moving Average Exponential'], timeperiod=smoothing_length)
elif type_ma == "EMA":
    df['Smoothing Line'] = talib.EMA(df['Moving Average Exponential'], timeperiod=smoothing_length)
elif type_ma == "SMMA (RMA)":
    df['Smoothing Line'] = talib.RMA(df['Moving Average Exponential'], timeperiod=smoothing_length)
elif type_ma == "WMA":
    df['Smoothing Line'] = talib.WMA(df['Moving Average Exponential'], timeperiod=smoothing_length)
elif type_ma == "VWMA":
    df['Smoothing Line'] = talib.VWMA(df['Moving Average Exponential'], timeperiod=smoothing_length)

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False) 
