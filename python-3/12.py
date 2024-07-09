import pandas as pd
import numpy as np
import talib as ta

# Load CSV data
df = pd.read_csv('data.csv')

# --- Function Definitions --- 

def normalization(src, mean):
    norm = (src - mean) / ta.STDDEV(src, timeperiod=200)
    norm[norm > 5] = 5
    norm[norm < -5] = -5
    return norm

def rescale(src, old_min, old_max, new_min, new_max):
    return new_min + (new_max - new_min) * (src - old_min) / max(old_max - old_min, 1e-10)

def regression_line(data, length):
    x = np.arange(len(data)).astype(np.float64)  # Convert x to float64
    y = (data['high'] + data['low']) / 2  
    x_ = ta.SMA(x, timeperiod=length)
    y_ = ta.SMA(y, timeperiod=length)
    mx = ta.STDDEV(x, timeperiod=length)
    my = ta.STDDEV(y, timeperiod=length)
    c = ta.CORREL(x, y, timeperiod=length)
    slope = c * (my / mx)
    inter = y_ - slope * x_
    return x * slope + inter


# --- User Inputs ---
length = 200
heat_sensative = 70

# --- Calculations ---
df['Regression_Line'] = regression_line(df, length)
df['color_level'] = normalization(df['close'] - df['Regression_Line'], 0)
df['Heat Map Seasons'] = rescale(df['color_level'], -4, 5, 0, 30)

# Save to CSV
df.to_csv('data.csv', index=False)
