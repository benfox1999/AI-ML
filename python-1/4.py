import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define strategy function
def channel_breakout_strategy(df, length=5):
    df['upBound'] = df['high'].rolling(window=length).max()
    df['downBound'] = df['low'].rolling(window=length).min()

    # Initialize buy/sell signals
    df['ChannelBreakOutStrategy-buy'] = np.nan
    df['ChannelBreakOutStrategy-sell'] = np.nan

    for i in range(length, len(df)):
        if not pd.isna(df['close'][i - length]):
            # Entry conditions
            if df['close'][i] > df['upBound'][i]:
                df['ChannelBreakOutStrategy-buy'][i] = 1
            if df['close'][i] < df['downBound'][i]:
                df['ChannelBreakOutStrategy-sell'][i] = 1

    return df

# Apply strategy
df = channel_breakout_strategy(df)

# Save updated DataFrame to CSV
df.to_csv('data.csv', index=False)
