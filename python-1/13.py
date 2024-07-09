import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define strategy parameters
length = 9
confirmBars = 1

# Calculate SMA
df['ma'] = talib.SMA(df['close'], timeperiod=length)

# Initialize buy/sell condition counters as pd.Series
df['bcount'] = pd.Series(0, index=df.index)
df['scount'] = pd.Series(0, index=df.index)

# Generate buy/sell signals (using .loc for assignment)
for i in range(length, len(df)):
    # Buy condition
    if df['close'][i] > df['ma'][i]:
        df.loc[i, 'bcount'] = df['bcount'][i - 1] + 1
    else:
        df.loc[i, 'bcount'] = 0

    # Sell condition
    if df['close'][i] < df['ma'][i]:
        df.loc[i, 'scount'] = df['scount'][i - 1] + 1
    else:
        df.loc[i, 'scount'] = 0

# Generate strategy entry signals
df['MACrossLE'] = np.where(df['bcount'] == confirmBars, 1, 0)
df['MACrossSE'] = np.where(df['scount'] == confirmBars, 1, 0)

# Save the updated DataFrame to a CSV file
df.to_csv('data.csv', index=False)
