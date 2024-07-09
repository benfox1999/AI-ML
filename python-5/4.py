import pandas as pd
import numpy as np
from ta.volatility import AverageTrueRange
from ta.trend import EMAIndicator
from ta.volume import VolumeWeightedAveragePrice

# Load your data from CSV
df = pd.read_csv('data.csv')

# Input Parameters (Adjust these)
fibonacci_level = 0.382 
atr_multiplier = 3
use_ema = True
ema_length = 20
use_vwap = True

# Function to detect swing highs and lows (mimicking fractals)
def get_swing_high_low(data, lookback=10):
    swing_high = data['high'].rolling(lookback).max()
    swing_low = data['low'].rolling(lookback).min()
    return swing_high, swing_low

# Find Swing Highs and Lows
swing_high, swing_low = get_swing_high_low(df)

# Initialize Fibonacci Levels (will be updated dynamically)
df['Fib_High'] = np.nan
df['Fib_Low'] = np.nan

# Determine Trend and Calculate Fibonacci Levels
for i in range(1, len(df)):
    if (swing_high[i] != swing_high[i-1]) and (swing_high[i] is not np.nan):
        df.loc[i:, 'Fib_High'] = swing_high[i]  # Use .loc for assignment
        df.loc[i:, 'Fib_Low'] = swing_low[i]
    elif (swing_low[i] != swing_low[i-1]) and (swing_low[i] is not np.nan):
        df.loc[i:, 'Fib_High'] = swing_low[i]
        df.loc[i:, 'Fib_Low'] = swing_high[i]


df['Fib_Level'] = df['Fib_High'] * (1 - fibonacci_level)

# Confluence Checks
atr = AverageTrueRange(high=df['high'], low=df['low'], close=df['close'])
df['ATR'] = atr.average_true_range()

df['isPriceNearFib'] = (df['close'] - df['Fib_Level']).abs() < df['ATR'] * 0.5

if use_ema:
    ema_indicator = EMAIndicator(close=df['close'], window=ema_length)
    df['EMA'] = ema_indicator.ema_indicator()
    df['emaConfluence'] = (df['close'] > df['EMA']) & (df['EMA'] > df['Fib_Level'])
else:
    df['emaConfluence'] = True

if use_vwap:
    vwap_indicator = VolumeWeightedAveragePrice(high=df['high'], low=df['low'], close=df['close'], volume=df['volume'])
    df['VWAP'] = vwap_indicator.volume_weighted_average_price()
    df['vwapConfluence'] = (df['close'] > df['VWAP']) & (df['VWAP'] > df['Fib_Level'])
else:
    df['vwapConfluence'] = True

# Long/Short Entry Signals
df['Fib_Level-longEntry'] = (
    ((swing_high != swing_high.shift(1)) | (swing_low != swing_low.shift(1))) &  # Fractal change
    df['isPriceNearFib'] & 
    df['emaConfluence'] &
    df['vwapConfluence']
)


# Save updated DataFrame back to CSV
df.to_csv('data.csv', index=False)
