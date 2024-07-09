import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Calculate HL2 (High-Low Average)
df['hl2'] = (df['high'] + df['low']) / 2

def normalize(src, length):
    """Normalization function equivalent to Pine Script's."""
    mean = talib.SMA(src, length)
    std = talib.STDDEV(src, length)
    norm = (src - mean) / std
    norm[norm > 5] = 5
    norm[norm < -5] = -5
    return norm

def regression_line(data, length):
    """Regression line calculation."""
    x = np.arange(len(data))
    y = data['hl2']
    x_ = talib.SMA(x.astype(float), length)
    y_ = talib.SMA(y, length)
    mx = talib.STDDEV(x.astype(float), length)
    my = talib.STDDEV(y, length)
    c = talib.CORREL(x.astype(float), y, length)
    slope = c * (my / mx)
    inter = y_ - slope * x_
    return x * slope + inter

# User Inputs (adjust as needed)
length = 200
heat_sensative = 70

# Calculate Regression Line
df['Regression_Line'] = regression_line(df, length)

# Calculate Color Level
df['color_level'] = normalize(df['close'] - df['Regression_Line'], length)

# Determine 'Heat Map Seasons' signal
df['Heat Map Seasons'] = np.where(df['color_level'] > 0, 1, 0)  # 1 for buy, 0 for sell 

# Save the updated DataFrame to the CSV
df.to_csv('data.csv', index=False) 
