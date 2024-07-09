import pandas as pd
import numpy as np
import talib

# Load data from CSV
data = pd.read_csv("data.csv")

# Define strategy parameters
length = 14
overSold = 30
overBought = 70

# Calculate RSI
data['rsi'] = talib.RSI(data['close'], timeperiod=length)

# Identify buy and sell signals
data['RsiLE'] = np.where(
    (data['rsi'] < overSold) & (data['rsi'].shift(1) >= overSold), 1, 0)
data['RsiSE'] = np.where(
    (data['rsi'] > overBought) & (data['rsi'].shift(1) <= overBought), 1, 0)

# Save the updated DataFrame to a CSV file
data.to_csv("data.csv", index=False)
