import pandas as pd
import numpy as np
import talib

# Load CSV data
data = pd.read_csv("data.csv")

# CM_Parabolic SAR Settings (matching Pine Script inputs)
start = 2 * 0.01
increment = 2 * 0.01
maximum = 2 * 0.10

# Calculate Parabolic SAR using TA-Lib
data['CM_Parabolic SAR-buy'] = talib.SAR(data['high'].values, data['low'].values, acceleration=increment, maximum=maximum)
data['CM_Parabolic SAR-sell'] = talib.SAR(data['high'].values, data['low'].values, acceleration=increment, maximum=maximum)

# Save the updated DataFrame to 'data.csv'
data.to_csv("data.csv", index=False)
