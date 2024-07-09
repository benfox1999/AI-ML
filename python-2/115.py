import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define SMMA function
def smma(src, length):
    # Convert src to numpy array and ensure float64 type for TA-Lib
    src = src.to_numpy(dtype='float64')

    smma_values = np.empty_like(src)
    smma_values[0:length] = np.nan

    # Handle empty SMA results
    sma_result = talib.SMA(src, length)
    if len(sma_result) > 0:
        smma_values[length] = sma_result[-1]
    else:
        smma_values[length] = np.nan

    # Ensure that smma_values is contiguous in memory
    smma_values = np.ascontiguousarray(smma_values)

    for i in range(length + 1, len(src)):
        smma_values[i] = (smma_values[i - 1] * (length - 1) + src[i]) / length
   
    return pd.Series(smma_values)  # Convert to Series

# Alligator parameters
jaw_length = 13
teeth_length = 8
lips_length = 5
jaw_offset = 8
teeth_offset = 5
lips_offset = 3

# Calculate HL2 (average of high and low)
df['hl2'] = (df['high'] + df['low']) / 2

# Calculate Alligator lines (convert smma result to Series before shifting)
df['Jaw'] = smma(df['hl2'], jaw_length).shift(jaw_offset)
df['Teeth'] = smma(df['hl2'], teeth_length).shift(teeth_offset)
df['Lips'] = smma(df['hl2'], lips_length).shift(lips_offset)

# Save the updated DataFrame to 'data.csv'
df.to_csv('data.csv', index=False)
