import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define function for SMA/EMA calculation
def esma(source, length, exp):
    if exp:
        return talib.EMA(source, length)
    else:
        return talib.SMA(source, length)

# Input parameters (matching Pine Script defaults)
shortlen = 10
longlen = 21
src = df['close']  # Use 'close' column as source
exp = False  

# Calculate short and long EMA/SMA
df['short'] = esma(src, shortlen, exp)
df['long'] = esma(src, longlen, exp)

# Calculate Price Oscillator (PO)
df['OSC'] = (df['short'] - df['long']) / df['long'] * 100

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False) 
