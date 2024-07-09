import pandas as pd
import numpy as np
import talib

# Load the CSV file into a pandas DataFrame
data = pd.read_csv('data.csv')

# Define the TSI function
def tsi(close, period):
    # Convert both input arrays to float64 before passing to TALib
    close_float = close.astype('float64')
    timeperiod_float = np.arange(len(close), dtype='float64')

    # Ensure that the arrays are contiguous in memory (required for TALib)
    close_float = np.ascontiguousarray(close_float)
    timeperiod_float = np.ascontiguousarray(timeperiod_float)

    return talib.CORREL(close_float, timeperiod_float, period) * 100

# Calculate the TSI indicator
data['Trend Strength Index'] = tsi(data['close'], period=14)

# Save the updated DataFrame to the CSV file
data.to_csv('data.csv', index=False)

