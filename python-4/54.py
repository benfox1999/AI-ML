import pandas as pd
import numpy as np
import talib

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

# Define the input parameters
fastperiod = 50
emaperiod = 100

# Calculate the true range and average true range
df['toc'] = np.maximum(df['open'], df['close'])
df['boc'] = np.minimum(df['open'], df['close'])

df['effclose'] = np.where(df['close'] >= df['open'], df['toc'], df['boc'])
# Calculate the EMA of the typical price
df['midline'] = df['effclose'].ewm(span=emaperiod, adjust=False).mean()

# Calculate the standard deviation of the typical price
df['dev'] = df['effclose'].rolling(window=emaperiod).std()

# Calculate the upper and lower bands
df['plusdevmult'] = np.where(df['toc'] > df['midline'], (df['toc'] - df['midline']) / df['dev'], 0)
df['minusdevmult'] = np.where(df['boc'] < df['midline'], (df['midline'] - df['boc']) / df['dev'], 0)

df['maxmult'] = df[['minusdevmult', 'plusdevmult']].max(axis=1)

# Calculate the EMA of the maximum multiplier
df['lm'] = df['maxmult'].ewm(span=emaperiod, adjust=False).mean()
df['lm2'] = df['lm'] / 2
df['lm3'] = df['lm2'] * 0.38196601
df['lm4'] = df['lm'] * 1.38196601
df['lm5'] = df['lm'] * 1.61803399
df['lm6'] = (df['lm'] + df['lm2']) / 2


# Calculate the Fibonacci levels
df['Fibonacci levels-6 up'] = df['midline'] + (df['dev'] * df['lm5'])
df['Fibonacci levels-5 up'] = df['midline'] + (df['dev'] * df['lm4'])
df['Fibonacci levels-4 up'] = df['midline'] + (df['dev'] * df['lm'])
df['Fibonacci levels-3 up'] = df['midline'] + (df['dev'] * df['lm6'])
df['Fibonacci levels-2 up'] = df['midline'] + (df['dev'] * df['lm2'])
df['Fibonacci levels-1 up'] = df['midline'] + (df['dev'] * df['lm3'])
df['Fibonacci levels-1 down'] = df['midline'] - (df['dev'] * df['lm3'])
df['Fibonacci levels-2 down'] = df['midline'] - (df['dev'] * df['lm2'])
df['Fibonacci levels-3 down'] = df['midline'] - (df['dev'] * df['lm6'])
df['Fibonacci levels-4 down'] = df['midline'] - (df['dev'] * df['lm'])
df['Fibonacci levels-5 down'] = df['midline'] - (df['dev'] * df['lm4'])
df['Fibonacci levels-6 down'] = df['midline'] - (df['dev'] * df['lm5'])

# Save the updated DataFrame to a new CSV file
df.to_csv('data.csv', index=False)
