import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Settings (matching Pine Script inputs)
length = 130
coef = 0.2
vcoef = 2.5
signalLength = 5
smoothVFI = False 

# Calculate typical price
df['typical'] = talib.TYPPRICE(df['high'], df['low'], df['close'])

# Calculate inter and vinter
df['inter'] = np.log(df['typical']) - np.log(df['typical'].shift(1))
df['vinter'] = df['inter'].rolling(window=30).std()

# Calculate cutoff, vave, vmax, and vc
df['cutoff'] = coef * df['vinter'] * df['close']
df['vave'] = df['volume'].rolling(window=length).mean()
df['vmax'] = df['vave'] * vcoef
df['vc'] = np.where(df['volume'] < df['vmax'], df['volume'], df['vmax'])

# Calculate mf and vcp
df['mf'] = df['typical'] - df['typical'].shift(1)
df['vcp'] = np.where(df['mf'] > df['cutoff'], df['vc'], 
                      np.where(df['mf'] < -df['cutoff'], -df['vc'], 0))

# Calculate vfi and vfima
df['vfi'] = (df['vcp'].rolling(window=length).sum() / df['vave']).rolling(window=3).mean() if smoothVFI else (df['vcp'].rolling(window=length).sum() / df['vave'])
df['vfima'] = talib.EMA(df['vfi'], timeperiod=signalLength)

# Calculate 'Volume Flow Indicator [LazyBear]' 
df['Volume Flow Indicator [LazyBear]'] = df['vfi'] - df['vfima'] 

# Save the updated DataFrame to data.csv
df.to_csv('data.csv', index=False)
