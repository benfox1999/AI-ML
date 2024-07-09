import pandas as pd
import numpy as np
import talib

# Load the CSV data
df = pd.read_csv('data.csv')

# Convert timestamps to datetime objects if needed
# df['open_time'] = pd.to_datetime(df['open_time'])
# df['close_time'] = pd.to_datetime(df['close_time'])

# Function to calculate percentage change
def changePercentString(value, close):
    round_val = (value / close) * 100 - 100
    return f"{( '+' if round_val >= 0 else '' )}{round_val:.2f}%"

# Placeholder for target price date (replace with actual logic)
df['target_price_date'] = pd.to_datetime('2024-03-08')  

# Calculate year from now based on target date
df['YearFromNow'] = df['target_price_date'] + pd.DateOffset(years=1)

# Placeholder for target prices (replace with your prediction model)
df['target_price_high'] = df['close'] * 1.10  # Example: 10% increase
df['target_price_average'] = df['close'] * 1.05  # Example: 5% increase
df['target_price_low'] = df['close'] * 0.95   # Example: 5% decrease

# Apply the changePercentString function
df['Price target-1'] = df.apply(lambda row: changePercentString(row['target_price_high'], row['close']), axis=1)
df['Price target-2'] = df.apply(lambda row: changePercentString(row['target_price_average'], row['close']), axis=1)
df['Price target-3'] = df.apply(lambda row: changePercentString(row['target_price_low'], row['close']), axis=1)

# Save the updated DataFrame to the CSV
df.to_csv('data.csv', index=False)
