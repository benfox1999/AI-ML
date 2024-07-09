import pandas as pd
import numpy as np
import talib

# Load the CSV data
data = pd.read_csv("data.csv")

# Calculate the High-Low-Close 3 (HLC3)
data['hlc3'] = (data['high'] + data['low'] + data['close']) / 3

# Calculate the volume multiplier
data['sv'] = np.where(data['hlc3'].diff() >= 0, data['volume'], -data['volume'])

# Calculate the Klinger Oscillator (KVO)
data['Klinger Oscillator-1'] = talib.EMA(data['sv'], timeperiod=34) - talib.EMA(data['sv'], timeperiod=55)

# Calculate the Signal line
data['Klinger Oscillator-2'] = talib.EMA(data['Klinger Oscillator-1'], timeperiod=13)

# Save the updated DataFrame to the CSV
data.to_csv("data.csv", index=False)
