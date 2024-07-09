import pandas as pd
import numpy as np
import talib

# Load data from CSV
data = pd.read_csv("data.csv")

# Bollinger Bands calculation
length = 20
mult = 2.0
# Calculate SMA (basis)
data['Bollinger Bands-1'] = data['close'].rolling(window=length).mean()
# Calculate standard deviation
data['Bollinger Bands-2'] = data['close'].rolling(window=length).std() * mult
# Calculate upper and lower bands
data['Bollinger Bands-3'] = data['Bollinger Bands-1'] + data['Bollinger Bands-2']
data['Bollinger Bands-4'] = data['Bollinger Bands-1'] - data['Bollinger Bands-2']

# Save the updated DataFrame to the same CSV file
data.to_csv("data.csv", index=False)
