import pandas as pd
import numpy as np


# Load CSV data with type conversion for specific columns
df = pd.read_csv('data.csv', dtype={'14': float, '15': float, '354': float}, low_memory=False)


# Custom Pivot High and Low Functions
def pivot_high(data, left, right):
    pivots = pd.Series(np.nan, index=data.index)
    for i in range(left + right, len(data)):
        window = data.iloc[i - (left + right) : i + 1]
        if data.iloc[i] == window.max() and data.iloc[i] > window.iloc[-right - 2]:
            pivots.iloc[i] = data.iloc[i]
    return pivots


def pivot_low(data, left, right):
    pivots = pd.Series(np.nan, index=data.index)
    for i in range(left + right, len(data)):
        window = data.iloc[i - (left + right) : i + 1]
        if data.iloc[i] == window.min() and data.iloc[i] < window.iloc[-right - 2]:
            pivots.iloc[i] = data.iloc[i]
    return pivots

# Define the Pine Script input parameters
leftLenH = 10
rightLenH = 10
leftLenL = 10
rightLenL = 10

# Calculate Pivot High
df['ph'] = pivot_high(df['high'], leftLenH, rightLenH)

# Calculate Pivot Low
df['pl'] = pivot_low(df['low'], leftLenL, rightLenL)

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)  # Remove the index when saving to CSV
