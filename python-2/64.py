import pandas as pd
import numpy as np
import talib

# Load the CSV data
df = pd.read_csv('data.csv')

# Calculate Net Volume
df['close_change'] = df['close'].diff()
df['NV'] = np.sign(df['close_change']) * df['volume']

# Save the updated DataFrame to the CSV
df.to_csv('data.csv', index=False)
