import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# RSI Calculation
def calculate_rsi(data, period):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Input parameters
rsi_length = 14
ma_type = "SMA"
ma_length = 14
bb_mult = 2.0
lookback_right = 5
lookback_left = 5
range_upper = 60
range_lower = 5

# Calculate RSI
df['Relative Strength Index'] = calculate_rsi(df['close'], rsi_length)

# Moving Average Calculation
if ma_type == "SMA":
    df['Relative Strength Index-1'] = df['Relative Strength Index'].rolling(window=ma_length).mean()
elif ma_type == "EMA":
    df['Relative Strength Index-1'] = df['Relative Strength Index'].ewm(span=ma_length, adjust=False).mean()
# Add other MA types as needed (Bollinger Bands, SMMA, WMA, VWMA)

# Bollinger Bands
if ma_type == "Bollinger Bands":
    std_dev = df['Relative Strength Index'].rolling(window=ma_length).std()
    df['Upper Bollinger Band'] = df['Relative Strength Index-1'] + std_dev * bb_mult
    df['Lower Bollinger Band'] = df['Relative Strength Index-1'] - std_dev * bb_mult


#Pivot Points Calculation (Implementing custom pivot point logic)
def pivot_high(data, left, right):
    pivots = []
    for i in range(left, len(data)-right):
        window = data[i-left:i+right+1]  # Include the current index
        if window.max() == data[i]:
            pivots.append(data[i])
        else:
            pivots.append(np.nan)
    pivots = [np.nan]*left + pivots + [np.nan]*right  # Add NaNs to the beginning and end
    return pd.Series(pivots, index=data.index)

def pivot_low(data, left, right):
    pivots = []
    for i in range(left, len(data)-right):
        window = data[i-left:i+right+1]
        if window.min() == data[i]:
            pivots.append(data[i])
        else:
            pivots.append(np.nan)
    pivots = [np.nan]*left + pivots + [np.nan]*right
    return pd.Series(pivots, index=data.index)

df['pivot_low'] = pivot_low(df['Relative Strength Index'], left=lookback_left, right=lookback_right)
df['pivot_high'] = pivot_high(df['Relative Strength Index'], left=lookback_left, right=lookback_right)


# Divergence Calculation 
def detect_divergence(df, rsi_col, price_col, lookback, pivot_type='high', range_upper=70, range_lower=30):
    divergence = [np.nan] * lookback  # Initialize with NaNs for initial values

    for i in range(lookback, len(df)):
        if range_lower < df[rsi_col][i] < range_upper:
            divergence.append(np.nan)
            continue

        # Get recent RSI and price values
        recent_rsi = df[rsi_col][i - lookback: i + 1]
        recent_price = df[price_col][i - lookback: i + 1]

        # Find pivot point, handling missing values
        if pivot_type == 'high':
            pivot_index = recent_rsi.idxmax(skipna=True)
        else:
            pivot_index = recent_rsi.idxmin(skipna=True)

        # Check for missing pivot and handle it
        if pd.isna(pivot_index):
            divergence.append(np.nan)
            continue

        # Check for divergence
        if ((pivot_type == 'high' and recent_rsi.iloc[-1] < recent_rsi[pivot_index] and recent_price.iloc[-1] > recent_price[pivot_index]) or
            (pivot_type == 'low' and recent_rsi.iloc[-1] > recent_rsi[pivot_index] and recent_price.iloc[-1] < recent_price[pivot_index])):
            divergence.append(True)  # Divergence found
        else:
            divergence.append(np.nan)  # No divergence

    return pd.Series(divergence, index=df.index)  # Return as a Series to match the DataFrame index



df['Regular Bearish'] = detect_divergence(df, 'Relative Strength Index', 'close', lookback_right, 'high', range_upper, range_lower)
df['Regular Bullish'] = detect_divergence(df, 'Relative Strength Index', 'close', lookback_right, 'low', range_upper, range_lower)

# ... Add more logic for Hidden Bullish and Hidden Bearish as needed

# Generate alert signals
df['Alert'] = np.where(df['Regular Bullish'] | df['Regular Bearish'], True, False)  # Simplified alert condition

# Save to CSV
df.to_csv('data.csv', index=False)
