import pandas as pd
import numpy as np
import talib

# Load CSV data with type conversions
df = pd.read_csv('data.csv', dtype={'14': float, '15': float, '354': float}, low_memory=False)

# Define the Pine Script functions (modified for TA-Lib)
def dirmov(high, low, length):
    up = high.diff()
    down = -low.diff()
    close = df['close']
    plusDM = np.where((up > down) & (up > 0), up, 0)
    minusDM = np.where((down > up) & (down > 0), down, 0)
    truerange = talib.TRANGE(high, low, close)  # Remove timeperiod argument
    plus = 100 * talib.SMA(plusDM, timeperiod=length) / truerange
    minus = 100 * talib.SMA(minusDM, timeperiod=length) / truerange
    return plus, minus

def adx(high, low, close, diLength, adxLength):
    plus, minus = dirmov(high, low, diLength)
    sum_pm = plus + minus
    adx = 100 * talib.SMA(np.abs(plus - minus) / np.where(sum_pm == 0, 1, sum_pm), timeperiod=adxLength)
    return adx

# Calculate ADX
adxlen = 14 
dilen = 14

# Convert necessary columns to float64 (required by TA-Lib)
df['high'] = pd.to_numeric(df['high'], errors='coerce')
df['low'] = pd.to_numeric(df['low'], errors='coerce')
df['close'] = pd.to_numeric(df['close'], errors='coerce')

# Calculate and fill missing values with 0 to prevent errors
df['Average Directional Index'] = adx(df['high'].fillna(0), df['low'].fillna(0), df['close'].fillna(0), dilen, adxlen)

# Save the updated DataFrame to 'data.csv'
df.to_csv('data.csv', index=False)
