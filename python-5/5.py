import pandas as pd
from ta.momentum import RSIIndicator
import numpy as np
# Load your data from CSV (replace 'your_data.csv' with your actual file name)
df = pd.read_csv('data.csv')

# RSI Calculation
rsi_length = 14 
rsi_indicator = RSIIndicator(close=df['close'], window=rsi_length)
df['chatgpt-RSI'] = rsi_indicator.rsi()

# Parameters for slope and duration
duration_threshold = 5
slope_threshold = 2.0

# Initialize columns to track RSI time (using `np.nan` for missing values)
df['chatgpt-rsi_below_30_time'] = np.nan
df['chatgpt-rsi_above_70_time'] = np.nan
df['chatgpt-rsi_slope'] = np.nan

# Track time RSI spends below 30 and above 70 (using .loc)
for i in range(1, len(df)):
    if df.loc[i, 'chatgpt-RSI'] < 30:
        df.loc[i, 'chatgpt-rsi_below_30_time'] = (df.loc[i-1, 'chatgpt-rsi_below_30_time'] + 1) if not pd.isna(df.loc[i-1, 'chatgpt-rsi_below_30_time']) else 1
        df.loc[i, 'chatgpt-rsi_above_70_time'] = 0  
    elif df.loc[i, 'chatgpt-RSI'] > 70:
        df.loc[i, 'chatgpt-rsi_above_70_time'] = (df.loc[i-1, 'chatgpt-rsi_above_70_time'] + 1) if not pd.isna(df.loc[i-1, 'chatgpt-rsi_above_70_time']) else 1
        df.loc[i, 'chatgpt-rsi_below_30_time'] = 0
    else:
        df.loc[i, 'chatgpt-rsi_below_30_time'] = 0
        df.loc[i, 'chatgpt-rsi_above_70_time'] = 0

    # Calculate slope of RSI (only if enough data is available)
    if i >= rsi_length:
        df.loc[i, 'chatgpt-rsi_slope'] = (df.loc[i, 'chatgpt-RSI'] - df.loc[i - rsi_length, 'chatgpt-RSI']) / rsi_length

# Buy/Sell Signals (using .loc)
df['chatgpt-buy_signal'] = (
    (df['chatgpt-RSI'] > 30) & 
    (df['chatgpt-RSI'].shift(1) <= 30) & 
    (df['chatgpt-rsi_below_30_time'] >= duration_threshold) &
    (df['chatgpt-rsi_slope'] >= slope_threshold)
)

df['chatgpt-sell_signal-01'] = (
    (df['chatgpt-RSI'] < 70) & 
    (df['chatgpt-RSI'].shift(1) >= 70) & 
    (df['chatgpt-rsi_above_70_time'] >= duration_threshold) &
    (df['chatgpt-rsi_slope'] <= -slope_threshold)
)

# Save updated DataFrame back to CSV
df.to_csv('data.csv', index=False)  # Save to