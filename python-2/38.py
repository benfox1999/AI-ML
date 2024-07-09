import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Calculate Ease of Movement (EOM)
length = 14  # Pine Script input
divisor = 10000  # Pine Script input

df['hl2'] = (df['high'] + df['low']) / 2
df['EOM'] = divisor * ((df['hl2'] - df['hl2'].shift(1)) * (df['high'] - df['low'])) / df['volume']
df['EOM'] = talib.SMA(df['EOM'].fillna(0), timeperiod=length)

# Save updated DataFrame to CSV
df.to_csv('data.csv', index=False) 
