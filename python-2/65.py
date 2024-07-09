import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Calculate On Balance Volume (OBV)
df['On Balance Volume'] = np.where(df['close'].diff() > 0, df['volume'], np.where(df['close'].diff() < 0, -df['volume'], 0)).cumsum()

# Define smoothing function
def apply_ma(data, length, type_ma):
    if type_ma == "SMA":
        return talib.SMA(data, length)
    elif type_ma == "EMA":
        return talib.EMA(data, length)
    elif type_ma == "SMMA (RMA)":
        return talib.RMA(data, length)
    elif type_ma == "WMA":
        return talib.WMA(data, length)
    elif type_ma == "VWMA":
        return talib.VWMA(data, length)
    else:
        raise ValueError("Invalid moving average type")

# Calculate smoothing line for OBV
smoothing_length = 5  # Replace with desired smoothing length
smoothing_type = "SMA"  # Replace with desired smoothing type ("SMA", "EMA", "SMMA (RMA)", "WMA", "VWMA")
df['On Balance Volume-1'] = apply_ma(df['On Balance Volume'], smoothing_length, smoothing_type)

# Save updated data to CSV
df.to_csv('data.csv', index=False)
