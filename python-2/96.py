import pandas as pd
import numpy as np
import talib

# Load the CSV file
data = pd.read_csv('data.csv')

# Define the TEMA function
def calculate_tema(data, length):
  ema1 = talib.EMA(data['close'], timeperiod=length)
  ema2 = talib.EMA(ema1, timeperiod=length)
  ema3 = talib.EMA(ema2, timeperiod=length)
  return 3 * (ema1 - ema2) + ema3

# Calculate TEMA and add it to the DataFrame
data['Triple EMA'] = calculate_tema(data, length=9)

# Save the updated DataFrame to the CSV file
data.to_csv('data.csv', index=False)
