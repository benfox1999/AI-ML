import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Pine Script Inputs
period = 21  # input.int(21, title="Length", minval=1)
isCentered = False  # input(false, title="Centered")

# Calculate SMA
df['ma'] = talib.SMA(df['close'], timeperiod=period)

# Calculate barsback
barsback = period / 2 + 1

# Calculate DPO
if isCentered:
    df['Detrended Price Oscillator'] = df['close'].shift(int(barsback)) - df['ma']
else:
    df['Detrended Price Oscillator'] = df['close'] - df['ma'].shift(int(barsback))

# Save updated DataFrame to CSV
df.to_csv('data.csv', index=False)
