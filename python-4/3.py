import pandas as pd
import numpy as np
import talib

# Load CSV data
data = pd.read_csv('data.csv')

# Input parameters (replace with user inputs if needed)
pd_period = 22
bbl_length = 20
mult = 2.0
lb_period = 50
ph_level = 0.85
pl_level = 1.01

# Calculate Williams Vix Fix
data['wvf'] = ((data['high'].rolling(pd_period).max() - data['low']) / data['high'].rolling(pd_period).max()) * 100

# Calculate Bollinger Bands
data['midLine'] = data['wvf'].rolling(bbl_length).mean()
data['sDev'] = mult * data['wvf'].rolling(bbl_length).std()
data['upperBand'] = data['midLine'] + data['sDev']
data['lowerBand'] = data['midLine'] - data['sDev']

# Calculate Range High and Range Low
data['rangeHigh'] = data['wvf'].rolling(lb_period).max() * ph_level
data['rangeLow'] = data['wvf'].rolling(lb_period).min() * pl_level

# Generate buy/sell signals
data['CM_Williams_Vix_Fix'] = np.where((data['wvf'] >= data['upperBand']) | (data['wvf'] >= data['rangeHigh']), 1, 0)

# Save the updated DataFrame to a CSV file
data.to_csv('data.csv', index=False) 
