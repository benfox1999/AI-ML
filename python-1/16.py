import pandas as pd
import numpy as np
import talib

# Load the CSV file into a Pandas DataFrame
data = pd.read_csv('data.csv')

# Define the Pine Script input parameters
leftBars = 4
rightBars = 2

# Calculate pivot highs and lows
data['ph'] = data['high'].rolling(window = leftBars + rightBars + 1).apply(lambda x: x[:-rightBars - 1].max(), raw = True).shift(-rightBars)
data['pl'] = data['low'].rolling(window = leftBars + rightBars + 1).apply(lambda x: x[:-rightBars - 1].min(), raw = True).shift(-rightBars)

# Generate trading signals
data['PivExtLE'] = np.where(data['pl'] > 0, 1, 0)
data['PivExtSE'] = np.where(data['ph'] > 0, 1, 0)

# Save the updated DataFrame to a CSV file
data.to_csv('data.csv', index=False)
