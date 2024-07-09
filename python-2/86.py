import pandas as pd
import numpy as np
import talib

# Load the CSV file
data = pd.read_csv("data.csv")

# Define the input parameters
longlen = 20
shortlen = 5
siglen = 5

# Custom TSI Function
def TSI(close, shortlen=13, longlen=25):
    momentum = close.diff()
    absolute_momentum = abs(momentum)

    smoothed_momentum = momentum.ewm(span=shortlen, adjust=False).mean().ewm(span=longlen, adjust=False).mean()
    smoothed_abs_momentum = absolute_momentum.ewm(span=shortlen, adjust=False).mean().ewm(span=longlen, adjust=False).mean()
    tsi = 100 * (smoothed_momentum / smoothed_abs_momentum)
    return tsi

# Calculate the SMI Ergodic Oscillator
data['tsi'] = TSI(data['close'], shortlen, longlen)
data['sig'] = data['tsi'].rolling(window=siglen).mean()
data['SMI Ergodic Oscillator'] = data['tsi'] - data['sig']

# Save the updated DataFrame to the CSV file
data.to_csv("data.csv", index=False)
