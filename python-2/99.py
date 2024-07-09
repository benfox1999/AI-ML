import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define Pine Script input parameters
length1 = 7
length2 = 14
length3 = 28

# Calculate Ultimate Oscillator
def calculate_uo(df, length1, length2, length3):
    df['high_'] = np.maximum(df['high'], df['close'].shift(1))
    df['low_'] = np.minimum(df['low'], df['close'].shift(1))
    df['bp'] = df['close'] - df['low_']
    df['tr_'] = df['high_'] - df['low_']

    df['avg7'] = talib.SUM(df['bp'], timeperiod=length1) / talib.SUM(df['tr_'], timeperiod=length1)
    df['avg14'] = talib.SUM(df['bp'], timeperiod=length2) / talib.SUM(df['tr_'], timeperiod=length2)
    df['avg28'] = talib.SUM(df['bp'], timeperiod=length3) / talib.SUM(df['tr_'], timeperiod=length3)
    df['Ultimate Oscillator'] = 100 * (4*df['avg7'] + 2*df['avg14'] + df['avg28']) / 7
    return df

# Calculate and append the indicator to the DataFrame
df = calculate_uo(df, length1, length2, length3)

# Save the updated DataFrame to CSV
df.to_csv('data.csv', index=False)
