import pandas as pd
import numpy as np
import talib

# Load CSV data with type conversions and handle potential mixed types
data = pd.read_csv("data.csv", dtype={'14': float, '15': float, '354': float}, low_memory=False)

# Chande Kroll Stop Parameters 
p = 10 
x = 1 
q = 9 

# Calculate ATR (correcting timeperiod argument)
data['ATR'] = talib.ATR(data['high'], data['low'], data['close'], timeperiod=p)

# Convert columns to numeric (for calculations and to handle potential errors)
data['high'] = pd.to_numeric(data['high'], errors='coerce').fillna(0)
data['low'] = pd.to_numeric(data['low'], errors='coerce').fillna(0)
data['close'] = pd.to_numeric(data['close'], errors='coerce').fillna(0)
data['ATR'] = pd.to_numeric(data['ATR'], errors='coerce').fillna(0)

# Calculate First High/Low Stops
data['first_high_stop'] = data['high'].rolling(p).max() - x * data['ATR']
data['first_low_stop'] = data['low'].rolling(p).min() + x * data['ATR']

# Calculate Stop Long/Short
data['Chande Kroll Stop-1'] = data['first_high_stop'].rolling(q).max()
data['Chande Kroll Stop-2'] = data['first_low_stop'].rolling(q).min()

# Save the updated DataFrame back to CSV
data.to_csv("data.csv", index=False)
