import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define KST function
def kst_indicator(data, roclen1=10, roclen2=15, roclen3=20, roclen4=30,
                  smalen1=10, smalen2=10, smalen3=10, smalen4=15, siglen=9):
    # Calculate rate of change (ROC)
    roc1 = talib.ROC(data['close'], timeperiod=roclen1)
    roc2 = talib.ROC(data['close'], timeperiod=roclen2)
    roc3 = talib.ROC(data['close'], timeperiod=roclen3)
    roc4 = talib.ROC(data['close'], timeperiod=roclen4)

    # Calculate smoothed ROC
    smaroc1 = talib.SMA(roc1, timeperiod=smalen1)
    smaroc2 = talib.SMA(roc2, timeperiod=smalen2)
    smaroc3 = talib.SMA(roc3, timeperiod=smalen3)
    smaroc4 = talib.SMA(roc4, timeperiod=smalen4)

    # Calculate KST and signal line
    kst = smaroc1 + 2 * smaroc2 + 3 * smaroc3 + 4 * smaroc4
    signal = talib.SMA(kst, timeperiod=siglen)
    
    return kst, signal

# Calculate KST and signal
df['Know Sure Thing-1'], df['Know Sure Thing-2'] = kst_indicator(df)

# Save updated DataFrame to CSV
df.to_csv('data.csv', index=False)
