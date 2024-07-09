import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Calculate ATR
df['ATR'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=10)

# Calculate Supertrend
def calculate_supertrend(df, factor, atr_period):
    atr = df['ATR']
    high = df['high']
    low = df['low']
    close = df['close']

    # Calculate basic upper and lower bands
    basic_upper_band = ((high + low) / 2) + (factor * atr)
    basic_lower_band = ((high + low) / 2) - (factor * atr)

    # Initialize Supertrend and direction
    supertrend = np.full(len(df), np.nan)
    direction = np.full(len(df), np.nan)

    # Calculate Supertrend and direction
    for i in range(atr_period, len(df)):
        prev_supertrend = supertrend[i - 1]
        prev_direction = direction[i - 1] if i > atr_period else 1

        if prev_direction == 1:
            if close[i] <= prev_supertrend:
                supertrend[i] = basic_lower_band[i]
                direction[i] = -1
            else:
                supertrend[i] = min(prev_supertrend, basic_lower_band[i])
                direction[i] = 1
        else:
            if close[i] >= prev_supertrend:
                supertrend[i] = basic_upper_band[i]
                direction[i] = 1
            else:
                supertrend[i] = max(prev_supertrend, basic_upper_band[i])
                direction[i] = -1

    return supertrend, direction

# Calculate Supertrend and direction
df['Supertrend'], df['Direction'] = calculate_supertrend(df, factor=3.0, atr_period=10)

# Save updated DataFrame to CSV
df.to_csv('data.csv', index=False)
