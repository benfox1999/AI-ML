import pandas as pd
import numpy as np
import talib

# Load CSV data with type conversion for specific columns
df = pd.read_csv('data.csv', dtype={'14': float, '15': float, '354': float}, low_memory=False) 

# Define Pine Script functions in Python (corrected)
def dirmov(high, low, length):
    up = high.diff()
    down = -low.diff()
    truerange = talib.TRANGE(high, low, close=df['close'])
    plus = 100 * talib.SMA(np.where((up > down) & (up > 0), up, 0), length) / truerange
    minus = 100 * talib.SMA(np.where((down > up) & (down > 0), down, 0), length) / truerange
    return plus, minus

def adx(high, low, close, diLength, adxLength):
    plus, minus = dirmov(high, low, diLength)
    sum_pm = plus + minus
    adx_val = 100 * talib.SMA(np.abs(plus - minus) / np.where(sum_pm == 0, 1, sum_pm), adxLength)
    return adx_val

# Define input parameters
adxSmoothPeriod = 14 
adxPeriod = 14
adxLowerLevel = 18
profitTargetMultiple = 1  # Not used in the current code
stopLossMultiple = 0.5   # Not used in the current code
boxLookBack = 20
enableDirection = 0  # 0: both buy/sell, 1: buy only, -1: sell only

# Calculate ADX
df['adx'] = adx(df['high'], df['low'], df['close'], adxSmoothPeriod, adxPeriod)

# Identify consolidation periods
df['isADXLow'] = df['adx'] < adxLowerLevel

# Calculate breakout box levels (vectorized)
def calculate_box_levels(df):
    box_start = df['isADXLow'].ne(df['isADXLow'].shift(1)) & df['isADXLow']
    df['boxUpperLevel'] = df['high'].where(box_start).ffill()
    df['boxLowerLevel'] = df['low'].where(box_start).ffill()
    return df

df = df.groupby(df['isADXLow'].cumsum()).apply(calculate_box_levels)

# Calculate box width
df['boxWidth'] = df['boxUpperLevel'] - df['boxLowerLevel']

# Initialize trade signals
df['ADX Breakout-buy'] = False
df['ADX Breakout-sell'] = False

# Generate trading signals (vectorized)
df['ADX Breakout-buy'] = (
    df['isADXLow']
    & (df['close'] > df['boxUpperLevel'])
    & (enableDirection >= 0)  # Enable buy signal based on enableDirection
)

df['ADX Breakout-sell'] = (
    df['isADXLow']
    & (df['close'] < df['boxLowerLevel'])
    & (enableDirection <= 0)  # Enable sell signal based on enableDirection
)

# Save the updated DataFrame to a CSV file
df.to_csv('data.csv', index=False)
