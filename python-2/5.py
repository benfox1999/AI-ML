import pandas as pd
import numpy as np

# Load CSV data with type conversion for specific columns
df = pd.read_csv('data.csv', dtype={'14': float, '15': float, '354': float}, low_memory=False) 

# Calculate 'Advance/Decline Ratio (Bars)'
length = 9

# Create 'isUp' column as a pandas Series
df['isUp'] = pd.Series(np.where((df['close'] - df['open']) >= 0.0, 1, 0), index=df.index)

# Apply rolling sum to the 'isUp' Series
df['upBars'] = df['isUp'].rolling(window=length, min_periods=1).sum()

# Create a Series for down bars
df['downBars'] = (1 - df['isUp']).rolling(window=length, min_periods=1).sum()

# Calculate the ratio using pd.Series operations
df['Advance/Decline Ratio (Bars)'] = df['upBars'] / df['downBars'].replace(0, 1)

# Save updated DataFrame to CSV
df.to_csv('data.csv', index=False)
