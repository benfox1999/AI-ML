import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv', dtype={'14': float, '15': float, '354': float}, low_memory=False)

# Pine Script Inputs (Modify as needed)
source_column = 'hl2'
length = 3
atr_length = 14
atr_mult = 2

# Calculate 'hl2' if it's not already in the DataFrame
if 'hl2' not in df.columns:
    df['hl2'] = (df['high'] + df['low']) / 2

# Convert columns to numeric type to handle potential non-numeric values
df['high'] = pd.to_numeric(df['high'], errors='coerce')
df['low'] = pd.to_numeric(df['low'], errors='coerce')
df['close'] = pd.to_numeric(df['close'], errors='coerce')
df['hl2'] = pd.to_numeric(df['hl2'], errors='coerce')

# Calculate Median
df['Median'] = (df['high'] + df['low']) / 2  # MEDPRICE is simply (high + low) / 2

# Calculate ATR (using timeperiod argument)
df['ATR'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=atr_length)

# Calculate Upper and Lower Bands
df['Upper Band'] = df['Median'] + atr_mult * df['ATR']
df['Lower Band'] = df['Median'] - atr_mult * df['ATR']

# Calculate Median EMA
df['Median EMA'] = talib.EMA(df['Median'], timeperiod=length)

# Save the updated DataFrame to CSV
df.to_csv('data.csv', index=False)
