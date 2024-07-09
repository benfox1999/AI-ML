import pandas as pd
import numpy as np
import talib

# Load data from CSV
df = pd.read_csv('data.csv')

# Define Inputs
tp = 10  
sl = 10  
maxidf = 5  

# Initialize Strategy Columns (with pd.Series to avoid warnings)
df['Greedy Strategy'] = pd.Series(np.nan, index=df.index) 

# Calculate Indicators
df['upGap'] = df['open'] > df['high'].shift(1)
df['dnGap'] = df['open'] < df['low'].shift(1)

# Initialize Position Tracking Variables
position_size = 0

# Iterate through Data (use .loc for assignments)
for i in range(1, len(df)):
    # Update Position
    if not np.isnan(df['Greedy Strategy'][i-1]):
        position_size = 1 if df['Greedy Strategy'][i-1] == 1 else -1 if df['Greedy Strategy'][i-1] == -1 else 0
    else:
        position_size = 0

    # Calculate Entry/Exit Signals
    if df['upGap'][i] and position_size == 0:
        df.loc[i, 'Greedy Strategy'] = 1  # Enter Long
    elif df['open'][i] > df['close'][i] and position_size < 0:
        df.loc[i, 'Greedy Strategy'] = -1  # Enter Short
    elif df['dnGap'][i] and position_size == 0:
        df.loc[i, 'Greedy Strategy'] = -1  # Enter Short
    elif df['open'][i] < df['close'][i] and position_size > 0:
        df.loc[i, 'Greedy Strategy'] = 1  # Enter Long 
    else:
        df.loc[i, 'Greedy Strategy'] = np.nan  # No Trade

# Save the updated DataFrame back to the CSV
df.to_csv('data.csv', index=False)
