import pandas as pd
import numpy as np

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

# Define the Pine Script input parameters
consecutive_bars_up = 3
consecutive_bars_down = 3

# Calculate 'ups' and 'dns' columns (initialized as pd.Series to avoid the warning)
df['ups'] = pd.Series(0, index=df.index)
df['dns'] = pd.Series(0, index=df.index)

# Use `.loc` for explicit index-based assignments
for i in range(1, len(df)):
    if df['close'][i] > df['close'][i - 1]:
        df.loc[i, 'ups'] = df['ups'][i - 1] + 1
    else:
        df.loc[i, 'ups'] = 0

    if df['close'][i] < df['close'][i - 1]:
        df.loc[i, 'dns'] = df['dns'][i - 1] + 1
    else:
        df.loc[i, 'dns'] = 0

# Create columns for buy and sell signals
df['Consecutive Up/Down Strategy-buy'] = np.where(df['ups'] >= consecutive_bars_up, 1, 0)
df['Consecutive Up/Down Strategy-sell'] = np.where(df['dns'] >= consecutive_bars_down, 1, 0)

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)
