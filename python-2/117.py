import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define the Williams %R calculation function
def calculate_williams_percent_r(close, length):
    max_high = close.rolling(window=length).max()
    min_low = close.rolling(window=length).min()
    return 100 * (close - max_high) / (max_high - min_low)

# Calculate Williams %R
df['Williams %R'] = calculate_williams_percent_r(df['close'], length=14)

# Save the updated DataFrame to 'data.csv'
df.to_csv('data.csv', index=False)
