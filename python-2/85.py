import pandas as pd
import numpy as np
import talib

# Load CSV data
data = pd.read_csv("data.csv")

# Define Pine Script input variables
longlen = 20
shortlen = 5
siglen = 5

# Custom TSI Function
def TSI(close, shortlen=13, longlen=25):
    m = close.diff()
    m_abs = abs(m)
    pc = m.ewm(span=shortlen, adjust=False).mean().ewm(span=longlen, adjust=False).mean()
    apc = m_abs.ewm(span=shortlen, adjust=False).mean().ewm(span=longlen, adjust=False).mean()
    tsi = 100 * (pc / apc)
    return tsi

# Calculate SMI Ergodic Indicator (SMII)
data['tsi'] = TSI(data['close'], shortlen, longlen)  # Use custom TSI function
data['SMI Ergodic Indicator-1'] = data['tsi']
data['SMI Ergodic Indicator-2'] = data['tsi'].ewm(span=siglen, adjust=False).mean()

# Save the updated DataFrame to 'data.csv'
data.to_csv("data.csv", index=False)
