import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Convert timestamps to datetime objects if necessary
df['open_time'] = pd.to_datetime(df['open_time'])
df['close_time'] = pd.to_datetime(df['close_time'])

# --- WaveTrend Function ---
def calculate_wavetrend(df, channel_len, average_len, ma_len):
    df['esa'] = df['close'].ewm(span=channel_len, adjust=False).mean()
    df['de'] = abs(df['close'] - df['esa']).ewm(span=channel_len, adjust=False).mean()
    df['ci'] = (df['close'] - df['esa']) / (0.015 * df['de'])
    df['wt1'] = df['ci'].ewm(span=average_len, adjust=False).mean()
    df['wt2'] = df['wt1'].rolling(window=ma_len).mean()
    df['wtVwap'] = df['wt1'] - df['wt2']
    return df

# --- RSI+MFI Function ---
def calculate_rsimfi(df, period, multiplier):
    df['money_flow'] = ((df['close'] - df['open']) / (df['high'] - df['low'])) * multiplier
    df['rsiMFI'] = talib.SMA(df['money_flow'], period) - 2.5 
    return df

# --- Stochastic RSI Function ---
def calculate_stochrsi(df, stoch_len, rsi_len, smooth_k, smooth_d):
    df['rsi'] = talib.RSI(df['close'], timeperiod=rsi_len)
    df['stoch_k'], df['stoch_d'] = talib.STOCHRSI(df['rsi'], timeperiod=stoch_len, fastk_period=smooth_k, fastd_period=smooth_d)
    return df

# --- Divergence Function --- 
def find_divergences(df, src_column, window, ob_level, os_level):
    df['fractal_top'] = np.where((df[src_column].shift(4) < df[src_column].shift(2)) &
                               (df[src_column].shift(3) < df[src_column].shift(2)) &
                               (df[src_column].shift(2) > df[src_column].shift(1)) &
                               (df[src_column].shift(2) > df[src_column]), 1, 0)

    df['fractal_bot'] = np.where((df[src_column].shift(4) > df[src_column].shift(2)) &
                               (df[src_column].shift(3) > df[src_column].shift(2)) &
                               (df[src_column].shift(2) < df[src_column].shift(1)) &
                               (df[src_column].shift(2) < df[src_column]), -1, 0)

    df['high_prev'] = np.where(df['fractal_top'] == 1, df[src_column].shift(2), np.nan)
    df['high_prev'].fillna(method='ffill', inplace=True)

    df['low_prev'] = np.where(df['fractal_bot'] == -1, df[src_column].shift(2), np.nan)
    df['low_prev'].fillna(method='ffill', inplace=True)

    df['bear_div'] = np.where((df['fractal_top'] == 1) & 
                             (df[src_column] > ob_level) & 
                             (df[src_column] < df['high_prev']), 1, 0)

    df['bull_div'] = np.where((df['fractal_bot'] == -1) & 
                             (df[src_column] < os_level) & 
                             (df[src_column] > df['low_prev']), 1, 0)
    return df

# --- Calculate Indicators ---

# WaveTrend
df = calculate_wavetrend(df, channel_len=9, average_len=12, ma_len=3)

# RSI+MFI 
df = calculate_rsimfi(df, period=60, multiplier=150)

# Stochastic RSI
df = calculate_stochrsi(df, stoch_len=14, rsi_len=14, smooth_k=3, smooth_d=3)

# --- Divergences ---
df = find_divergences(df, 'wt2', window=10, ob_level=53, os_level=-53)  # Example parameters

# --- Buy/Sell Signals ---

# VuManChu B Divergences Strategy 
df['VuManChu B Divergences-buy'] = np.where(
    (df['wt1'] > df['wt2']) & (df['wt1'].shift(1) < df['wt2'].shift(1)) & (df['wt2'] < -53), 1, 0) 

df['VuManChu B Divergences-sell'] = np.where(
    (df['wt1'] < df['wt2']) & (df['wt1'].shift(1) > df['wt2'].shift(1)) & (df['wt2'] > 53), 1, 0)


# --- Save to CSV ---
df.to_csv('data.csv', index=False)
