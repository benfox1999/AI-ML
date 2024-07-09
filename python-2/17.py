import pandas as pd
import numpy as np
import talib

# Load CSV data
data = pd.read_csv("data.csv")

# Define Pine Script inputs
short_length = 20
long_length = 50
std_dev_mult = 2.0

# Calculate Bollinger Bands
data['short_middle'], data['short_upper'], data['short_lower'] = talib.BBANDS(
    data['close'], timeperiod=short_length, nbdevup=std_dev_mult, nbdevdn=std_dev_mult
)
data['long_middle'], data['long_upper'], data['long_lower'] = talib.BBANDS(
    data['close'], timeperiod=long_length, nbdevup=std_dev_mult, nbdevdn=std_dev_mult
)

# Calculate BBTrend
data['BBTrend'] = (
    (abs(data['short_lower'] - data['long_lower']) - abs(data['short_upper'] - data['long_upper']))
    / data['short_middle']
    * 100
)

# Save the updated DataFrame to 'data.csv'
data.to_csv("data.csv", index=False)
