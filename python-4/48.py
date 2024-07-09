import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Input parameters
length = 20
len2 = 10

# Calculate indicators
df['lower'] = df['low'].rolling(window=length).min()
df['upper'] = df['high'].rolling(window=length).max()

df['up'] = df['high'].rolling(window=length).max()
df['down'] = df['low'].rolling(window=length).min()
df['sup'] = df['high'].rolling(window=len2).max()
df['sdown'] = df['low'].rolling(window=len2).min()

# Calculate K1 (Trend Line)
df['K1'] = np.where(
    (df['high'].rolling(window=length).apply(lambda x: (x >= x.max()).idxmax() + 1).fillna(0) <=
     df['low'].rolling(window=length).apply(lambda x: (x <= x.min()).idxmax() + 1).fillna(0)),
    df['down'],
    df['up']
)

# Calculate K2 (Exit Line)
df['K2'] = np.where(
    (df['high'].rolling(window=length).apply(lambda x: (x >= x.max()).idxmax() + 1).fillna(0) <=
     df['low'].rolling(window=length).apply(lambda x: (x <= x.min()).idxmax() + 1).fillna(0)),
    df['sdown'],
    df['sup']
)

# Buy and Sell Signals
df['Turtle Trade Channels Indicator-buy'] = np.where(
    (df['high'] == df['upper'].shift(1)) | (df['high'] > df['upper'].shift(1)), 1, 0
)
df['Turtle Trade Channels Indicator-sell'] = np.where(
    (df['low'] == df['lower'].shift(1)) | (df['low'] < df['lower'].shift(1)), 1, 0
)

# Save updated data to CSV
df.to_csv('data.csv', index=False)
