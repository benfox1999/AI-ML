import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv', dtype={'14': float, '15': float, '354': float}, low_memory=False)

# --- Input Parameters (Modify as needed) ---
threshold_multiplier = 3.0
depth = 10
reverse = False
levelsFormat = "Values"
labelsPosition = "Left"


# --- ZigZag Implementation ---
def calculate_zigzag(df, threshold_multiplier, depth):
    df = df.copy()
    df['atr'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=10)
    df['devThreshold'] = df['atr'] / df['close'] * 100 * threshold_multiplier

    pivots = []
    trend = None
    last_pivot_idx = 0

    for i in range(depth, len(df)):
        high = df['high'].iloc[i - depth : i].max()
        low = df['low'].iloc[i - depth : i].min()

        if df['high'].iloc[i] > high and abs(df['high'].iloc[i] - high) > df['devThreshold'].iloc[i]:
            if trend != "up":
                if trend == "down":
                    pivots.append((last_pivot_idx, "down", df['low'].iloc[last_pivot_idx]))
                pivots.append((i, "up", df['high'].iloc[i]))
                last_pivot_idx = i
                trend = "up"

        elif df['low'].iloc[i] < low and abs(df['low'].iloc[i] - low) > df['devThreshold'].iloc[i]:
            if trend != "down":
                if trend == "up":
                    pivots.append((last_pivot_idx, "up", df['high'].iloc[last_pivot_idx]))
                pivots.append((i, "down", df['low'].iloc[i]))
                last_pivot_idx = i
                trend = "down"
    return pivots


# --- Fibonacci Calculation ---
def fibonacci_levels(start_price, end_price, levels=[0, 0.236, 0.382, 0.5, 0.618, 1, 1.618, 2.618]):
    diff = end_price - start_price
    return [start_price + (diff * level) for level in levels]


# Calculate ZigZag Pivots
pivots = calculate_zigzag(df.copy(), threshold_multiplier, depth)

# --- Main Calculation Logic ---
fib_level_columns = [f'Auto Fib Retracement-{i}' for i in range(8)]
for col in fib_level_columns:
    df[col] = np.nan

if pivots:
    for i in range(1, len(pivots)):
        idx1, type1, price1 = pivots[i - 1]
        idx2, type2, price2 = pivots[i]
        
        # Ensure we're calculating between a high and a low pivot
        if type1 != type2:
            start_price = price1
            end_price = price2

            if reverse:
                start_price, end_price = end_price, start_price

            fib_levels = fibonacci_levels(start_price, end_price)
            
            for j, level in enumerate(fib_levels):
                df.loc[idx1:idx2, fib_level_columns[j]] = level 

# Save to CSV
df.to_csv('data.csv', index=False)
