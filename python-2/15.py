import pandas as pd
import numpy as np
import talib

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

# Calculate the Awesome Oscillator (AO)
df['hl2'] = (df['high'] + df['low']) / 2
df['AO'] = talib.SMA(df['hl2'], timeperiod=5) - talib.SMA(df['hl2'], timeperiod=34)

# Calculate the difference between consecutive AO values
df['AO_diff'] = df['AO'] - df['AO'].shift(1)

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)
