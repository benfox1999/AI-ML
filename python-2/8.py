import pandas as pd
import numpy as np

# Load CSV data with type conversion for specific columns
df = pd.read_csv('data.csv', dtype={'14': float, '15': float, '354': float}, low_memory=False)

# --- Input Parameters (mimic Pine Script inputs) ---
depth = 10
reverse = False
prices = True
levels = True
levelsFormat = "Values"  # "Values" or "Percent"
labelsPosition = "Left"  # "Left" or "Right"


# --- ZigZag Implementation ---
def zigzag(df, column='high', dev=5/100):
    df = df.copy()
    up = df[column].diff() > 0
    dn = df[column].diff() < 0

    pivot_points = up.copy()
    pivot_points[0] = True

    last_pivot = df[column].iloc[0]
    last_pivot_idx = 0

    for i in range(1, len(df)):
        if up[i] and df[column].iloc[i] - last_pivot > dev * last_pivot:
            last_pivot = df[column].iloc[i]
            last_pivot_idx = i
            pivot_points[last_pivot_idx] = True
        elif dn[i] and last_pivot - df[column].iloc[i] > dev * last_pivot:
            last_pivot = df[column].iloc[i]
            last_pivot_idx = i
            pivot_points[last_pivot_idx] = True
        else:
            pivot_points[i] = False

    df['pivots'] = pivot_points

    # Remove intermediate pivot points
    filtered_pivots = df.loc[df['pivots'], column]
    last_pivot = filtered_pivots.iloc[0]

    for i in range(1, len(filtered_pivots)):
        if filtered_pivots.iloc[i] > last_pivot:
            df.loc[filtered_pivots.iloc[i - 1] : filtered_pivots.index[i], column] = filtered_pivots.iloc[i]
            last_pivot = filtered_pivots.iloc[i]
        elif filtered_pivots.iloc[i] < last_pivot:
            df.loc[filtered_pivots.iloc[i - 1] : filtered_pivots.index[i], column] = filtered_pivots.iloc[i]
            last_pivot = filtered_pivots.iloc[i]

    # Fill remaining values with NaN
    df.loc[~df['pivots'], column] = np.nan
    df.drop(columns=['pivots'], inplace=True)

    return df[column]

df['zigzag_high'] = zigzag(df.copy(), 'high', 0.05) 
df['zigzag_low'] = zigzag(df.copy(), 'low', 0.05)



# Find Pivots
def find_pivots(df, depth, isHigh):
    pivots = np.nan * np.ones(len(df))
    for i in range(depth, len(df)):
        window = df.iloc[i - depth:i]
        if isHigh:
            if df['high'].iloc[i] == window['high'].max():
                pivots[i] = df['high'].iloc[i]
        else:
            if df['low'].iloc[i] == window['low'].min():
                pivots[i] = df['low'].iloc[i]
    return pivots


df['pivots_high'] = find_pivots(df, depth // 2, True)
df['pivots_low'] = find_pivots(df, depth // 2, False)

# --- Auto Fib Extension Logic ---
def auto_fib_extension(df, depth):
    upperThreshold = 0.236
    lowerThreshold = 1.0
    end_prices = [np.nan] * depth  # Initialize with NaN for the initial rows

    for i in range(depth, len(df)):
        last_high_idx = np.where(~np.isnan(df['pivots_high'].iloc[i-depth:i].values))[0]
        last_low_idx = np.where(~np.isnan(df['pivots_low'].iloc[i-depth:i].values))[0]
        
        if last_high_idx.size > 0 and last_low_idx.size > 0:
            last_high_idx = last_high_idx[-1] + i - depth
            last_low_idx = last_low_idx[-1] + i - depth
            
            lastH = df['pivots_high'].iloc[last_high_idx]
            lastL = df['pivots_low'].iloc[last_low_idx]

            isHighLast = last_high_idx > last_low_idx

            if isHighLast:
                startPrice = lastL
                endPrice = lastH
                diff = abs(startPrice - endPrice)
                if not (endPrice + diff * lowerThreshold > lastH > endPrice + diff * upperThreshold):
                    endPrice = np.nan
            else:
                startPrice = lastH
                endPrice = lastL
                diff = abs(startPrice - endPrice)
                if not (endPrice - diff * lowerThreshold < lastL < endPrice - diff * upperThreshold):
                    endPrice = np.nan
        else:
            endPrice = np.nan

        end_prices.append(endPrice)

    return end_prices

# Apply the corrected function
df['Auto Fib Extension'] = auto_fib_extension(df, depth)


# --- Level Calculations & Output ---
def calculate_level(df, value, endPrice, diff):
    return endPrice + ((-1 if reverse else 1) * diff * value)

df['diff'] = abs(df['Auto Fib Extension'].shift(1) - df['close'].shift(1))

# Example for one level (repeat for other levels)
df['Auto Fib Extension-0.236'] = calculate_level(df, 0.236, df['Auto Fib Extension'], df['diff'])


# Save to CSV
df.to_csv('data.csv', index=False)
