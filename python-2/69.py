import pandas as pd
import numpy as np

# Load the CSV data, parsing the 'open_time' column as datetime
df = pd.read_csv('data.csv', parse_dates=['open_time'], infer_datetime_format=True)

# --- Pivot Point Calculation Functions ---

def _calculate_pivot_levels(high, low, close, pivot_type="Traditional"):
    if pivot_type == "Traditional":
        pp = (high + low + close) / 3
        r1 = 2 * pp - low
        s1 = 2 * pp - high
        r2 = pp + (high - low)
        s2 = pp - (high - low)
        r3 = pp + 2 * (high - low)
        s3 = pp - 2 * (high - low)
        r4 = pp + 3 * (high - low)  # Added R4 and S4 levels
        s4 = pp - 3 * (high - low)
        r5 = pp + 4 * (high - low)  # Added R5 and S5 levels
        s5 = pp - 4 * (high - low)
        return pp, r1, s1, r2, s2, r3, s3, r4, s4, r5, s5
    else:
        raise ValueError(f"Unsupported pivot_type: {pivot_type}")

def calculate_pivot_points(df, pivot_type="Traditional", pivot_timeframe="D", 
                           is_daily_based=True, max_historical_pivots=15):

    # Set 'open_time' as the index
    df.set_index('open_time', inplace=True)

    # Resample DataFrame to the desired timeframe
    if is_daily_based or pivot_timeframe == "D":
        df_resampled = df.resample('D').agg({'high': 'max', 'low': 'min', 'close': 'last'})
    # Add handling for other timeframes (e.g., 'W' for weekly, 'M' for monthly) as needed

    # Calculate pivot points for each period
    pivot_columns = ['P', 'R1', 'S1', 'R2', 'S2', 'R3', 'S3', 'R4', 'S4', 'R5', 'S5']  # Added more columns
    for col in pivot_columns:
        df[col] = np.nan  # Initialize columns in the original DataFrame

    for i in range(max(0, len(df_resampled) - max_historical_pivots), len(df_resampled)):
        high, low, close = df_resampled.loc[df_resampled.index[i], ['high', 'low', 'close']]
        pivots = _calculate_pivot_levels(high, low, close, pivot_type)
        df.loc[df_resampled.index[i], pivot_columns] = pivots

    # Reset index to bring back 'open_time' as a column
    df = df.reset_index()
    
    return df

# --- Main Execution ---

# Calculate Pivot Points 
df = calculate_pivot_points(df)

# Save the updated DataFrame to CSV
df.to_csv('data.csv', index=False)
