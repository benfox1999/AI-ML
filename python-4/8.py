import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Convert 'open_time' and 'close_time' to datetime objects if needed
df['open_time'] = pd.to_datetime(df['open_time'])
df['close_time'] = pd.to_datetime(df['close_time'])

def calculate_indicators(df, useCurrentRes=True, resCustom='D', len=20, factorT3=7, atype=1, 
                        doma2=False, len2=50, sfactorT3=7, atype2=1, spc=False, cc=True, smoothe=2,
                        spc2=False, cc2=True, warn=False, warn2=False, sd=False):
    """
    Calculates technical indicators from Pine Script logic.
    """

    # Resolution handling - Assuming 'period' maps to current DataFrame frequency
    res = df['open_time'].dt.strftime('%f')[0] if useCurrentRes else resCustom 

    # --- Moving Average Calculations ---
    def calculate_ma(src, length, ma_type, t3_factor=None):
        """Calculates various moving averages."""
        if ma_type == 1:
            return talib.SMA(src, length)
        elif ma_type == 2:
            return talib.EMA(src, length)
        elif ma_type == 3:
            return talib.WMA(src, length)
        elif ma_type == 4:
            return talib.WMA(2 * talib.WMA(src, length // 2) - talib.WMA(src, length), int(np.sqrt(length))) 
        elif ma_type == 5:
            return talib.VWMA(src, length)
        elif ma_type == 6:
            return talib.RSI(src, length)  # Placeholder: Pine Script's RMA is not in TA-Lib
        elif ma_type == 7:
            ema1 = talib.EMA(src, length)
            ema2 = talib.EMA(ema1, length)
            ema3 = talib.EMA(ema2, length)
            return 3 * (ema1 - ema2) + ema3
        elif ma_type == 8 and t3_factor is not None:
            factor = t3_factor * 0.1
            gd = lambda src, len: talib.EMA(src, len) * (1 + factor) - talib.EMA(talib.EMA(src, len), len) * factor
            return gd(gd(gd(src, length), length), length)
        else:
            return None  

    # Calculate primary moving average
    df['out1'] = calculate_ma(df['close'], len, atype, factorT3 if atype == 8 else None)
    df['out1'] = df['out1'].shift(1) # Account for lookback

    # Calculate secondary moving average (if enabled)
    if doma2:
        df['out2'] = calculate_ma(df['close'], len2, atype2, sfactorT3 if atype2 == 8 else None) 
        df['out2'] = df['out2'].shift(1)  # Account for lookback

    # --- Price Cross and Bar Color Logic ---
    if spc:
        df['CM_Ultimate_MA_MTF_V2'] = np.where((df['open'] < df['out1']) & (df['close'] > df['out1']), 1, 0)
    if spc2 and doma2:
        df['CM_Ultimate_MA_MTF_V2'] = np.where((df['open'] < df['out2']) & (df['close'] > df['out2']), 1, 0)

    return df  # Return the DataFrame with new columns

# --- Apply the calculations ---
df = calculate_indicators(df.copy()) # Create a copy to avoid modifying the original DataFrame in-place

# Save the updated DataFrame to the CSV
df.to_csv('data.csv', index=False) 
