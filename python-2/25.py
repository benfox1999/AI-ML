import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define CMO calculation function
def calculate_cmo(src, length):
    momm = src.diff()
    m1 = np.where(momm >= 0, momm, 0)
    m2 = np.where(momm < 0, -momm, 0)
    sm1 = talib.SUM(m1, timeperiod=length)
    sm2 = talib.SUM(m2, timeperiod=length)
    cmo = 100 * (sm1 - sm2) / (sm1 + sm2)
    return cmo

# Calculate Chande Momentum Oscillator
df['Chande MO'] = calculate_cmo(df['close'], length=9)

# Save updated data to CSV
df.to_csv('data.csv', index=False)
