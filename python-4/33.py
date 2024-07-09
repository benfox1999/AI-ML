import pandas as pd
import numpy as np
import talib

# Load data from CSV
data = pd.read_csv("data.csv")

# Define middleDonchian function
def middleDonchian(data, length):
    lower = data.rolling(window=length).min()
    upper = data.rolling(window=length).max()
    return (upper + lower) / 2

# Ichimoku settings
conversionPeriods = 9
basePeriods = 26
laggingSpan2Periods = 52
displacement = 26

# Calculate Ichimoku components
data['Tenkan'] = middleDonchian(data['close'], conversionPeriods)
data['Kijun'] = middleDonchian(data['close'], basePeriods)
data['xChikou'] = data['close'].shift(-displacement)
data['SenkouA'] = middleDonchian(data['close'].shift(displacement), laggingSpan2Periods)
data['SenkouB'] = ((data['Tenkan'].shift(displacement) + data['Kijun'].shift(displacement)) / 2)

# Save the updated DataFrame back to 'data.csv'
data.to_csv('data.csv', index=False)
