import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Parabolic SAR calculation
acceleration_factor = 0.02
maximum_acceleration = 0.2

df['Parabolic SAR'] = talib.SAR(df['high'].values, df['low'].values,
                                acceleration=acceleration_factor,
                                maximum=maximum_acceleration)

# Save the updated DataFrame to the CSV
df.to_csv('data.csv', index=False)
