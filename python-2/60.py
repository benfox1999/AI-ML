import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define a function to calculate various moving averages
def calculate_ma(data, length, ma_type):
    if ma_type == "SMA":
        return talib.SMA(data, timeperiod=length)
    elif ma_type == "EMA":
        return talib.EMA(data, timeperiod=length)
    elif ma_type == "SMMA (RMA)":
        return talib.RMA(data, timeperiod=length)
    elif ma_type == "WMA":
        return talib.WMA(data, timeperiod=length)
    elif ma_type == "VWMA":
        return talib.VWMA(data, timeperiod=length)
    else:
        return np.nan

# Moving Average 1
ma1_length = 20  
ma1_type = "SMA"  
df['Moving Average Ribbon-1'] = calculate_ma(df['close'], ma1_length, ma1_type)

# Moving Average 2
ma2_length = 50  
ma2_type = "SMA"  
df['Moving Average Ribbon-2'] = calculate_ma(df['close'], ma2_length, ma2_type)

# Moving Average 3
ma3_length = 100 
ma3_type = "SMA"  
df['Moving Average Ribbon-3'] = calculate_ma(df['close'], ma3_length, ma3_type)

# Moving Average 4
ma4_length = 200
ma4_type = "SMA"  
df['Moving Average Ribbon-4'] = calculate_ma(df['close'], ma4_length, ma4_type)

# Save the modified DataFrame to 'data.csv', overwriting the original file
df.to_csv('data.csv', index=False)
