import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define CCI function (Pine Script's ta.cci equivalent)
def CCI(df, period):
    tp = (df['high'] + df['low'] + df['close']) / 3
    return talib.CCI(df['high'], df['low'], df['close'], timeperiod=period)

# Calculate CCI indicators
df['CCI_Turbo'] = CCI(df, 6)
df['CCI_14'] = CCI(df, 14)

# Determine histogram color logic (adjust as needed)
df['histogram_color'] = np.where(
    (df['CCI_14'].shift(5) > 0) & 
    (df['CCI_14'].shift(4) > 0) & 
    (df['CCI_14'].shift(3) > 0) & 
    (df['CCI_14'].shift(2) > 0) & 
    (df['CCI_14'].shift(1) > 0), 
    '#009688', 
    np.where(
        (df['CCI_14'].shift(5) < 0) & 
        (df['CCI_14'].shift(4) < 0) & 
        (df['CCI_14'].shift(3) < 0) & 
        (df['CCI_14'].shift(2) < 0) & 
        (df['CCI_14'].shift(1) < 0),
        '#F44336',
        np.where(df['CCI_14'] < 0, '#009688', '#F44336')
    )
)

# Save the updated DataFrame to 'data.csv'
df.to_csv('data.csv', index=False)
