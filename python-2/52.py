import pandas as pd
import numpy as np
import talib

# Load data from CSV
df = pd.read_csv('data.csv')

# Calculate 'Mass Index'
length = 10  # Default value from Pine Script
df['span'] = df['high'] - df['low']
df['ema1'] = talib.EMA(df['span'], timeperiod=9)
df['ema2'] = talib.EMA(df['ema1'], timeperiod=9)
df['Mass Index'] = df['ema1'] / df['ema2']
df['Mass Index'] = df['Mass Index'].rolling(window=length).sum()

# Save updated DataFrame to CSV
df.to_csv('data.csv', index=False)
