import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Pine Script Inputs
wmaLength = 10
longRoCLength = 14
shortRoCLength = 11

# Calculate Coppock Curve
df['longROC'] = talib.ROC(df['close'], timeperiod=longRoCLength)
df['shortROC'] = talib.ROC(df['close'], timeperiod=shortRoCLength)
df['Coppock Curve'] = talib.WMA(df['longROC'] + df['shortROC'], timeperiod=wmaLength)

# Save updated DataFrame to CSV
df.to_csv('data.csv', index=False)
