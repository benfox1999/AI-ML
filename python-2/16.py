import pandas as pd
import numpy as np

# Load CSV data
df = pd.read_csv('data.csv')

# Calculate Balance of Power
df['Balance of Power'] = (df['close'] - df['open']) / (df['high'] - df['low'])

# Save updated data to CSV
df.to_csv('data.csv', index=False)
