import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Calculate SMA
df['SMA'] = talib.SMA(df['close'], timeperiod=20)

def calculate_dampened_projections(df, sma_window, acceleration_window, src_off, start_factor, growth_factor, prediction_length):
    # Calculate SMA slope and acceleration
    df['SMA_Slope'] = df['SMA'] - df['SMA'].shift(1)
    df['SMA_Acceleration'] = df['SMA'].rolling(window=acceleration_window).apply(
        lambda x: ((x - 2 * np.roll(x, 1) + np.roll(x, 2)).sum()) / acceleration_window, raw=True
    )

    # Generate dampened polynomial curves
    for i in range(-4, 5):
        damp_factor = start_factor + i * growth_factor
        for j in range(1, prediction_length + 1):
            df[f'ABDP_{i}_{j}'] = df['SMA'].shift(src_off) + df['SMA_Slope'].shift(src_off) * j + 0.5 * damp_factor * df['SMA_Acceleration'].shift(src_off) * j * j
    return df

# Apply calculations and save to CSV
df = calculate_dampened_projections(df, sma_window=20, acceleration_window=5, src_off=20, start_factor=0, growth_factor=0.5, prediction_length=10)
df.to_csv('data.csv', index=False)
