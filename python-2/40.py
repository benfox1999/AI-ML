import pandas as pd
import numpy as np
import talib

# Load the CSV file into a Pandas DataFrame
data = pd.read_csv('data.csv')

# Input parameters (mimicking Pine Script inputs)
length = 20
percent = 10.0
source = data['close']  # Using 'close' column as the source
exponential = False

# Calculate basis (SMA or EMA)
if exponential:
    basis = talib.EMA(source, timeperiod=length)
else:
    basis = talib.SMA(source, timeperiod=length)

# Calculate upper and lower bands
k = percent / 100.0
upper = basis * (1 + k)
lower = basis * (1 - k)

# Add the calculated columns to the DataFrame
data['Basis'] = basis
data['Upper'] = upper
data['Lower'] = lower

# Save the updated DataFrame to the CSV file
data.to_csv('data.csv', index=False) 
