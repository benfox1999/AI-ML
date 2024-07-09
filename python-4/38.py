import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Convert timestamp columns to datetime objects if needed
# df['open_time'] = pd.to_datetime(df['open_time']) 
# df['close_time'] = pd.to_datetime(df['close_time']) 

import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Convert timestamp columns to datetime objects if needed
# df['open_time'] = pd.to_datetime(df['open_time']) 
# df['close_time'] = pd.to_datetime(df['close_time']) 

def calculate_strategy(df, HiLoLen=34, fastEMAlength=89, mediumEMAlength=200, slowEMAlength=600, ShowFastEMA=True, 
                       ShowMediumEMA=True, ShowSlowEMA=False, ShowHHLL=False, ShowFractals=True, filterBW=False, 
                       ShowBarColor=True, ShowBuySell=True, Lookback=3, DelayArrow=False, ShowTrendBGcolor=True, 
                       UseHAcandles=True):
    """Calculates trading signals based on the provided Pine Script logic."""
    
    # Initialize Heikin Ashi columns
    df['ha_close'] = 0.0
    df['ha_open'] = 0.0
    df['ha_high'] = 0.0
    df['ha_low'] = 0.0

    # Heikin Ashi Calculations (if enabled)
    if UseHAcandles:
        df['ha_close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
        for i in range(len(df)):
            if i == 0:
                df.loc[i, 'ha_open'] = (df['open'][i] + df['close'][i]) / 2  # First bar
            else:
                df.loc[i, 'ha_open'] = (df['ha_open'][i - 1] + df['ha_close'][i - 1]) / 2
        df['ha_high'] = df[['ha_open', 'ha_close', 'high']].max(axis=1)
        df['ha_low'] = df[['ha_open', 'ha_close', 'low']].min(axis=1)
    else:
        df['ha_close'] = df['close']
        df['ha_open'] = df['open']
        df['ha_high'] = df['high']
        df['ha_low'] = df['low']

    # Moving Averages and PAC
    df['fastEMA'] = talib.EMA(df['ha_close'], timeperiod=fastEMAlength)
    df['mediumEMA'] = talib.EMA(df['ha_close'], timeperiod=mediumEMAlength)
    df['slowEMA'] = talib.EMA(df['ha_close'], timeperiod=slowEMAlength)
    df['pacC'] = talib.EMA(df['ha_close'], timeperiod=HiLoLen)
    df['pacL'] = talib.EMA(df['ha_low'], timeperiod=HiLoLen)
    df['pacU'] = talib.EMA(df['ha_high'], timeperiod=HiLoLen)


    # Trend Direction
    df['TrendDirection'] = np.where((df['fastEMA'] > df['mediumEMA']) & (df['pacL'] > df['mediumEMA']), 1,
                             np.where((df['fastEMA'] < df['mediumEMA']) & (df['pacU'] < df['mediumEMA']), -1, 0))

    # Fractal Recognition (simplified for clarity - might need adjustments)
    df['fractal_up'] = talib.MAX(df['high'], timeperiod=5).shift(-2) == df['high']
    df['fractal_down'] = talib.MIN(df['low'], timeperiod=5).shift(-2) == df['low']

    # Higher Highs, Lower Highs, etc. (simplified - might need adjustments)
    df['higher_high'] = (df['high'] > df['high'].shift(1)) & (df['high'].shift(1) > df['high'].shift(2))
    df['lower_high'] = (df['high'] < df['high'].shift(1)) & (df['high'].shift(1) < df['high'].shift(2))
    df['higher_low'] = (df['low'] > df['low'].shift(1)) & (df['low'].shift(1) > df['low'].shift(2))
    df['lower_low'] = (df['low'] < df['low'].shift(1)) & (df['low'].shift(1) < df['low'].shift(2))

    # Trading Logic
    Delay = 1 if DelayArrow else 0
    df['TradeDirection'] = 0  
    df['pacExitU'] = (df['ha_open'] < df['pacU']) & (df['ha_close'] > df['pacU']) & ((df['ha_close'] < df['pacC']).rolling(Lookback).sum() > 0)
    df['pacExitL'] = (df['ha_open'] > df['pacL']) & (df['ha_close'] < df['pacL']) & ((df['ha_close'] > df['pacC']).rolling(Lookback).sum() > 0)

    for i in range(1, len(df)):
        if df['TradeDirection'].iloc[i - 1] == 1 and df['ha_close'].iloc[i] < df['pacC'].iloc[i]:
            df.loc[i, 'TradeDirection'] = 0  # Use .loc for assignment
        elif df['TradeDirection'].iloc[i - 1] == -1 and df['ha_close'].iloc[i] > df['pacC'].iloc[i]:
            df.loc[i, 'TradeDirection'] = 0  # Use .loc for assignment
        elif df['TradeDirection'].iloc[i - 1] == 0 and (df['TrendDirection'].iloc[i] == 1 and df['pacExitU'].iloc[i]):
            df.loc[i, 'TradeDirection'] = 1  # Use .loc for assignment
        elif df['TradeDirection'].iloc[i - 1] == 0 and (df['TrendDirection'].iloc[i] == -1 and df['pacExitL'].iloc[i]):
            df.loc[i, 'TradeDirection'] = -1  # Use .loc for assignment
        else:
            df.loc[i, 'TradeDirection'] = df['TradeDirection'].iloc[i - 1]  # Use .loc for assignment

    return df

# Apply the strategy calculation
df = calculate_strategy(df)

# Save the updated DataFrame to CSV
df.to_csv('data.csv', index=False)
