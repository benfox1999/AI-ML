import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv("data.csv")

# Define RVGI function
def RVGI(df, length):
    df['close-open'] = df['close'] - df['open']
    df['high-low'] = df['high'] - df['low']
    df['RVGI-1'] = talib.SMA(talib.SMA(df['close-open'], length), length) / talib.SMA(talib.SMA(df['high-low'], length), length)
    df['RVGI-2'] = talib.SMA(df['RVGI-1'], length) 
    return df

# Calculate RVGI with length 10 
df = RVGI(df, 10)

# Save the updated DataFrame to data.csv
df.to_csv("data.csv", index=False)
