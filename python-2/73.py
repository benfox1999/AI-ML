import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Calculate Rate of Change (ROC)
length = 9
df['Rate Of Change'] = talib.ROC(df['close'], timeperiod=length) * 100

# Save the updated DataFrame to data.csv
df.to_csv('data.csv', index=False)
