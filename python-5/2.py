import pandas as pd
import numpy as np
import talib

# Load your data from CSV
df = pd.read_csv('data.csv')

# SMI Calculation using talib
def calculate_smi(df, window=14, smooth_period=3, smooth_signal=3):
    min_low = df['low'].rolling(window=window).min()
    max_high = df['high'].rolling(window=window).max()
    mid_point = (min_low + max_high) / 2
    df['smi'] = 100 * ((df['close'] - mid_point) / (max_high - min_low))
    df['smi_signal'] = df['smi'].rolling(window=smooth_signal).mean()
    return df

df = calculate_smi(df)

# Trend Filter (SMA)
df['Trend_SMA'] = talib.SMA(df['close'], timeperiod=50)
df['isUptrend'] = df['close'] > df['Trend_SMA']

# Long/Short Entry Signals
df['gemini-longEntry'] = ((df['smi'] > -20) & 
                  (df['smi'].shift(1) <= -20) & 
                  (df['isUptrend']))

df['gemini-shortEntry'] = ((df['smi'] < 20) & 
                   (df['smi'].shift(1) >= 20) & 
                   (df['isUptrend'] == False)) 

# Save updated DataFrame back to CSV
df.to_csv('data.csv', index=False)
