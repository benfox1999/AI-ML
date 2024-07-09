import pandas as pd
import numpy as np
import talib

# Load data from CSV
df = pd.read_csv('data.csv')

# Define Zig Zag function
def calculate_zigzag(df, deviation=5, depth=10):
    """
    Calculates Zig Zag points based on percentage deviation.

    Args:
        df (pd.DataFrame): DataFrame with 'high' and 'low' columns.
        deviation (float): Percentage deviation for reversals.
        depth (int): Minimum number of bars between peaks and valleys.

    Returns:
        pd.DataFrame: DataFrame with 'Zig Zag' column containing Zig Zag points.
    """

    df['Zig Zag'] = np.nan
    high_price = df['high'].iloc[0]
    low_price = df['low'].iloc[0]
    trend = None
    zigzag_index = 0

    for i in range(depth, len(df)):
        current_high = df['high'].iloc[i]
        current_low = df['low'].iloc[i]

        if trend == 'up':
            if current_high > high_price:
                high_price = current_high
                zigzag_index = i
            elif current_low < low_price * (1 - deviation / 100):
                df['Zig Zag'].iloc[zigzag_index] = high_price
                trend = 'down'
                low_price = current_low
                zigzag_index = i
        elif trend == 'down':
            if current_low < low_price:
                low_price = current_low
                zigzag_index = i
            elif current_high > high_price * (1 + deviation / 100):
                df['Zig Zag'].iloc[zigzag_index] = low_price
                trend = 'up'
                high_price = current_high
                zigzag_index = i
        else:
            if current_high >= df['high'].iloc[:i].max() * (1 + deviation / 100):
                trend = 'up'
                high_price = current_high
                zigzag_index = i
            elif current_low <= df['low'].iloc[:i].min() * (1 - deviation / 100):
                trend = 'down'
                low_price = current_low
                zigzag_index = i

    return df

# Calculate Zig Zag and append to DataFrame
df = calculate_zigzag(df, deviation=5, depth=10)

# Save updated DataFrame to CSV
df.to_csv('data.csv', index=False)
