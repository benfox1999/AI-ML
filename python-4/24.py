import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Parameter for pivot point calculation window
prd = 10

# Function to detect pivot highs and lows
def find_pivot_points(df, col_name, window=prd):
    pivot_points = pd.Series(np.nan, index=df.index)

    for i in range(window, len(df) - window):
        window_high = df[col_name].iloc[i - window: i + window + 1]
        if window_high.max() == df[col_name].iloc[i]:
            pivot_points.iloc[i] = df[col_name].iloc[i]

    return pivot_points

# Find Pivot Highs and Lows
df['pivot_high'] = find_pivot_points(df, 'high')
df['pivot_low'] = find_pivot_points(df, 'low')

# Calculate Center Line
df['center'] = df[['pivot_high', 'pivot_low']].mean(axis=1)
df['center'].fillna(method='ffill', inplace=True)

# Calculate ATR
df['atr'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=10)

# Calculate Upper and Lower Bands
factor = 3
df['up'] = df['center'] + (factor * df['atr'])
df['dn'] = df['center'] - (factor * df['atr'])

# Calculate SuperTrend (corrected)
df['final_upperband'] = np.nan  # Initialize with NaN
df['final_lowerband'] = np.nan  # Initialize with NaN
df['supertrend'] = np.nan  # Initialize with NaN

for i in range(len(df)):
    if i == 0:
        df.loc[i, 'final_upperband'] = 0.0
        df.loc[i, 'final_lowerband'] = 0.0
    else:
        if df['close'].iloc[i - 1] <= df['final_upperband'].iloc[i - 1]:
            df.loc[i, 'final_upperband'] = df['up'].iloc[i]
        else:
            df.loc[i, 'final_upperband'] = min(df['up'].iloc[i], df['final_upperband'].iloc[i - 1])
        
        if df['close'].iloc[i - 1] >= df['final_lowerband'].iloc[i - 1]:
            df.loc[i, 'final_lowerband'] = df['dn'].iloc[i]
        else:
            df.loc[i, 'final_lowerband'] = max(df['dn'].iloc[i], df['final_lowerband'].iloc[i - 1])

    df.loc[i, 'supertrend'] = df['final_lowerband'].iloc[i] if df['close'].iloc[i] > df['final_lowerband'].iloc[i] else df['final_upperband'].iloc[i]

# Buy/Sell Signals
df['Pivot Point SuperTrend-buy'] = (df['supertrend'] < df['close']) & (df['supertrend'].shift(1) > df['close'].shift(1))
df['Pivot Point SuperTrend-sell'] = (df['supertrend'] > df['close']) & (df['supertrend'].shift(1) < df['close'].shift(1))

# Save updated data to CSV
df.to_csv('data.csv', index=False)
