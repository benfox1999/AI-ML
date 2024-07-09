import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define SMMA function
def calculate_smma(src, length):
    smma = np.zeros_like(src)
    smma[length - 1] = np.mean(src[:length])
    for i in range(length, len(src)):
        smma[i] = (smma[i - 1] * (length - 1) + src[i]) / length
    return smma

# Calculate SMMA
df['Smoothed Moving Average'] = calculate_smma(df['close'], length=7)

# Save updated DataFrame to CSV
df.to_csv('data.csv', index=False)
