import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Arnaud Legoux Moving Average calculation
def alma(data, windowsize, offset, sigma):
    m = int(offset * (windowsize - 1))
    s = windowsize / sigma
    w = np.exp(-(np.arange(windowsize) - m)**2 / (2 * s**2))
    return np.convolve(data, w / w.sum(), 'valid')

# User Inputs (Matching Pine Script Defaults)
windowsize = 9
offset = 0.85
sigma = 6

# Calculate ALMA and add as a new column
df['Arnaud Legoux Moving Average'] = np.nan  # Initialize column with NaN
df['Arnaud Legoux Moving Average'][windowsize - 1:] = alma(
    df['close'], windowsize, offset, sigma
)

# Save the updated DataFrame back to CSV
df.to_csv('data.csv', index=False)
