import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Calculate DEMA
length = 9
df['e1'] = talib.EMA(df['close'], timeperiod=length)
df['e2'] = talib.EMA(df['e1'], timeperiod=length)
df['Double EMA'] = 2 * df['e1'] - df['e2']

# Save updated DataFrame to CSV
df.to_csv('data.csv', index=False)
