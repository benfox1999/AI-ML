import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define Pine Script input parameters
window1 = 8
window2 = 21

# Calculate support and resistance levels
def calculate_sr(df, window):
    df['high_highest'] = df['high'].rolling(window=window).max()
    df['low_lowest'] = df['low'].rolling(window=window).min()
    df['top'] = np.where(df['high'] >= df['high_highest'], df['high'], np.nan)
    df['bot'] = np.where(df['low'] <= df['low_lowest'], df['low'], np.nan)
    df['top'] = df['top'].ffill()
    df['bot'] = df['bot'].ffill()
    return df  # Return the modified DataFrame

# Calculate support and resistance, update the original DataFrame directly
df = calculate_sr(df, window1)  # Update df with results from the first calculation
df = calculate_sr(df, window2)  # Update df again with results from the second calculation

# Now you can safely drop the temporary columns
df.drop(['high_highest', 'low_lowest'], axis=1, inplace=True)

# Save updated data to CSV
df.to_csv('data.csv', index=False)
