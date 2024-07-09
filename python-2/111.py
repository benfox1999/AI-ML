import pandas as pd
import numpy as np
import talib

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

# Define the short and long lengths for the EMA calculations
shortlen = 5
longlen = 10

# Calculate the short and long EMAs using the 'talib' library
df['short'] = talib.EMA(df['volume'], timeperiod=shortlen)
df['long'] = talib.EMA(df['volume'], timeperiod=longlen)

# Calculate the Volume Oscillator
df['Volume Osc'] = 100 * (df['short'] - df['long']) / df['long']

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)
