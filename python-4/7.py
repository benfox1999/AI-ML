import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Input parameters (matching Pine Script defaults)
len_param = 14
th_param = 20

# Calculate indicators
df['TrueRange'] = np.maximum.reduce([
    df['high'] - df['low'],
    np.abs(df['high'] - df['close'].shift(1)),
    np.abs(df['low'] - df['close'].shift(1))
])

df['DirectionalMovementPlus'] = np.where(
    (df['high'] - df['high'].shift(1)) > (df['low'].shift(1) - df['low']),
    np.maximum(df['high'] - df['high'].shift(1), 0),
    0
)

df['DirectionalMovementMinus'] = np.where(
    (df['low'].shift(1) - df['low']) > (df['high'] - df['high'].shift(1)),
    np.maximum(df['low'].shift(1) - df['low'], 0),
    0
)

df['SmoothedTrueRange'] = talib.EMA(df['TrueRange'], timeperiod=len_param)
df['SmoothedDirectionalMovementPlus'] = talib.EMA(df['DirectionalMovementPlus'], timeperiod=len_param)
df['SmoothedDirectionalMovementMinus'] = talib.EMA(df['DirectionalMovementMinus'], timeperiod=len_param)

df['DIPlus'] = (df['SmoothedDirectionalMovementPlus'] / df['SmoothedTrueRange']) * 100
df['DIMinus'] = (df['SmoothedDirectionalMovementMinus'] / df['SmoothedTrueRange']) * 100
df['DX'] = (np.abs(df['DIPlus'] - df['DIMinus']) / (df['DIPlus'] + df['DIMinus'])) * 100
df['ADX'] = talib.SMA(df['DX'], timeperiod=len_param)

# Save the updated DataFrame to the same CSV file
df.to_csv('data.csv', index=False)
