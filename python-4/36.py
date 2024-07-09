import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Convert timestamps to datetime objects (if needed)
df['open_time'] = pd.to_datetime(df['open_time'])

# Define ZigZag function (Pine Script's zigzag is not directly available in TA-Lib)
def calculate_zigzag(df, zigzag_len):
    high_points = []
    high_indexes = []
    low_points = []
    low_indexes = []
    trend = 1
    last_trend_up_since = np.nan
    last_trend_down_since = np.nan

    for i in range(len(df)):
        high = df['high'][i]
        low = df['low'][i]

        to_up = high >= df['high'][max(0, i - zigzag_len + 1):i + 1].max()
        to_down = low <= df['low'][max(0, i - zigzag_len + 1):i + 1].min()

        if trend == 1 and to_down:
            trend = -1
            last_trend_down_since = i
        elif trend == -1 and to_up:
            trend = 1
            last_trend_up_since = i

        if not np.isnan(last_trend_up_since) and i - last_trend_up_since >= zigzag_len:
            low_val = df['low'][last_trend_up_since:i + 1].min()
            low_index = df['low'][last_trend_up_since:i + 1].idxmin()
            low_points.append(low_val)
            low_indexes.append(low_index)
            last_trend_up_since = np.nan

        if not np.isnan(last_trend_down_since) and i - last_trend_down_since >= zigzag_len:
            high_val = df['high'][last_trend_down_since:i + 1].max()
            high_index = df['high'][last_trend_down_since:i + 1].idxmax()
            high_points.append(high_val)
            high_indexes.append(high_index)
            last_trend_down_since = np.nan

    return high_points, high_indexes, low_points, low_indexes


# Set Pine Script input parameters
zigzag_len = 9  
fib_factor = 0.33 

# Calculate ZigZag
high_points, high_indexes, low_points, low_indexes = calculate_zigzag(df, zigzag_len)

# Initialize columns for MSB and Order Blocks
df['Market Structure Break & Order Block'] = 0
df['bu_ob_since'] = 0
df['be_ob_since'] = 0
df['be_bb_since'] = 0
df['bu_bb_since'] = 0

# Iterate through data to find MSB and Order Blocks
market = 1
last_l0 = np.nan
last_h0 = np.nan
bu_ob_index = 0
be_ob_index = 0
be_bb_index = 0
bu_bb_index = 0

for i in range(zigzag_len, len(df)):
    # ... (Logic to determine market structure break, order block identification - 
    # this part requires adapting the Pine Script logic to Python using the calculated 
    # high/low points and indexes, and potentially additional TA-Lib functions if needed)

    # Example for MSB (adapt based on your Pine Script logic):
    if i in high_indexes and market == -1:
        market = 1
        df.loc[i, 'Market Structure Break & Order Block'] = 1 
        # ... (Additional logic for box creation, labels, etc., can be added here)

    elif i in low_indexes and market == 1:
        market = -1
        df.loc[i, 'Market Structure Break & Order Block'] = -1
        # ... (Additional logic for box creation, labels, etc., can be added here)
    
    # Example for Order Block (adapt based on your Pine Script logic):
   


# Save the updated DataFrame to CSV
df.to_csv('data.csv', index=False) 
