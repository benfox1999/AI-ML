import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Momentum calculation
length = 10  # Equivalent to Pine Script's 'len' input
df['Momentum'] = df['close'] - df['close'].shift(length)

# Save the updated DataFrame back to CSV
df.to_csv('data.csv', index=False) 
