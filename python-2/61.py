import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# --- Pine Script to Python Conversion ---

# Input parameters (replicating Pine Script inputs)
len_ma = 9  # Length for Moving Average
src = df['close']  # Source data
offset = 0  # Offset (not used for calculations)

# Calculate Simple Moving Average (SMA)
df['Moving Average Simple'] = talib.SMA(src, timeperiod=len_ma)

# Function to calculate various moving averages (replicating Pine Script function 'ma')
def calculate_ma(source, length, ma_type):
    if ma_type == "SMA":
        return talib.SMA(source, timeperiod=length)
    elif ma_type == "EMA":
        return talib.EMA(source, timeperiod=length)
    elif ma_type == "SMMA (RMA)":
        return talib.RMA(source, timeperiod=length)
    elif ma_type == "WMA":
        return talib.WMA(source, timeperiod=length)
    elif ma_type == "VWMA":
        return talib.VWMA(source, timeperiod=length)
    else:
        raise ValueError("Invalid Moving Average Type")

# Input parameters for smoothing
type_ma = "SMA"  # Moving average type for smoothing
smoothing_length = 5  # Length for smoothing

# Calculate smoothing line
df['Smoothing Line'] = calculate_ma(df['Moving Average Simple'], smoothing_length, type_ma)

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False) 
