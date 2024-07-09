import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define Choppiness Index function
def choppiness_index(high, low, close, length):
    atr = talib.ATR(high, low, close, timeperiod=length)
    high_low_range = high - low
    sum_atr = atr.rolling(window=length).sum()
    ci = 100 * np.log10(sum_atr / (high_low_range.rolling(window=length).max() - high_low_range.rolling(window=length).min())) / np.log10(length)
    return ci

# Calculate Choppiness Index and add to DataFrame
df['CHOP'] = choppiness_index(df['high'], df['low'], df['close'], length=14)

# Save updated DataFrame to CSV
df.to_csv('data.csv', index=False)
