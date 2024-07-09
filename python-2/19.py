import pandas as pd
import numpy as np
import talib

# Load CSV data
data = pd.read_csv("data.csv")

# Bollinger Bands %b Calculation
length = 20
src = data['close']
mult = 2.0

# Calculate Bollinger Bands
data['basis'] = talib.SMA(src, timeperiod=length)
data['dev'] = mult * talib.STDDEV(src, timeperiod=length)
data['upper'] = data['basis'] + data['dev']
data['lower'] = data['basis'] - data['dev']

# Calculate and add Bollinger Bands %b to the DataFrame
data['Bollinger Bands %b'] = (src - data['lower']) / (data['upper'] - data['lower'])

# Save the updated DataFrame to the CSV file
data.to_csv("data.csv", index=False) 
