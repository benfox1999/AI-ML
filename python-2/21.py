import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define the length input
lengthInput = 13

# Calculate EMA (Exponential Moving Average)
df['EMA'] = talib.EMA(df['close'], timeperiod=lengthInput)

# Calculate Bull Power and Bear Power
df['Bull Power'] = df['high'] - df['EMA']
df['Bear Power'] = df['low'] - df['EMA']

# Calculate Bull Bear Power (BBP)
df['BBPower'] = df['Bull Power'] + df['Bear Power']

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)
