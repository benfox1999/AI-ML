import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define Supertrend function
def Supertrend(df, periods=10, multiplier=3.0, change_atr=True):
    df['tr'] = talib.TRANGE(df['high'], df['low'], df['close'])
    df['atr2'] = df['tr'].rolling(periods).mean()
    df['atr'] = talib.ATR(df['high'], df['low'], df['close'], periods) if change_atr else df['atr2']
    df['up'] = df['high'] - (multiplier * df['atr'])
    df['dn'] = df['low'] + (multiplier * df['atr'])

    # Vectorized approach for Supertrend calculation
    up_list = [df['up'][0]]
    dn_list = [df['dn'][0]]
    trend = [1]

    for i in range(1, len(df)):
        up = max(df['up'][i], up_list[-1]) if df['close'][i - 1] > up_list[-1] else df['up'][i]
        dn = min(df['dn'][i], dn_list[-1]) if df['close'][i - 1] < dn_list[-1] else df['dn'][i]

        up_list.append(up)
        dn_list.append(dn)
        trend.append(1 if df['close'][i] > dn_list[-2] else -1 if df['close'][i] < up_list[-2] else trend[-1])

    df['Supertrend-trend'] = trend
    df['Supertrend-up'] = up_list
    df['Supertrend-dn'] = dn_list

    # Generate buy/sell signals
    df['Supertrend-buy'] = ((df['Supertrend-trend'] == 1) & (df['Supertrend-trend'].shift(1) == -1)).astype(int)
    df['Supertrend-sell'] = ((df['Supertrend-trend'] == -1) & (df['Supertrend-trend'].shift(1) == 1)).astype(int)

    return df

# Calculate Supertrend
df = Supertrend(df)

# Save updated data to CSV
df.to_csv('data.csv', index=False)
