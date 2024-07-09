import pandas as pd
import numpy as np
import talib

# Load the CSV file into a pandas DataFrame
data = pd.read_csv('data.csv')

# Calculate the Accumulation/Distribution indicator
data['Accumulation/Distribution'] = talib.AD(data['high'], data['low'], data['close'], data['volume'])

# Save the updated DataFrame to the CSV file
data.to_csv('data.csv', index=False)
