import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Bollinger BandWidth Calculation
length = 20
src = df['close']
mult = 2.0
expansionLengthInput = 125
contractionLengthInput = 125

df['basis'] = talib.SMA(src, timeperiod=length)
df['dev'] = mult * talib.STDDEV(src, timeperiod=length)
df['upper'] = df['basis'] + df['dev']
df['lower'] = df['basis'] - df['dev']
df['Bollinger BandWidth'] = ((df['upper'] - df['lower']) / df['basis']) * 100

# Highest Expansion and Lowest Contraction
df['Highest Expansion'] = df['Bollinger BandWidth'].rolling(window=expansionLengthInput).max()
df['Lowest Contraction'] = df['Bollinger BandWidth'].rolling(window=contractionLengthInput).min()

# Save the updated DataFrame to 'data.csv'
df.to_csv('data.csv', index=False) 
