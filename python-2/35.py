import pandas as pd
import numpy as np
import talib

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('data.csv')

# Define the input parameters
lensig = 14  # ADX Smoothing
len_di = 14  # DI Length

# Calculate True Range (TR)
df['tr'] = talib.TRANGE(df['high'], df['low'], df['close'])

# Calculate Upward Price Change
df['up'] = df['high'].diff()

# Calculate Downward Price Change
df['down'] = -df['low'].diff()

# Calculate Plus Directional Movement (+DM)
df['plusDM'] = np.where(np.logical_or(df['up'] <= 0, df['up'] <= df['down']), 0, df['up'])
df['plusDM'] = np.where(pd.isna(df['up']), np.nan, df['plusDM'])

# Calculate Minus Directional Movement (-DM)
df['minusDM'] = np.where(np.logical_or(df['down'] <= 0, df['down'] <= df['up']), 0, df['down'])
df['minusDM'] = np.where(pd.isna(df['down']), np.nan, df['minusDM'])

# Calculate True Range Moving Average (TRMA)
df['trur'] = talib.SMA(df['tr'], timeperiod=len_di)

# Calculate Plus Directional Index (+DI)
df['plus'] = 100 * talib.SMA(df['plusDM'], timeperiod=len_di) / df['trur']
df['plus'] = np.where(pd.isna(df['plus']), 0, df['plus'])

# Calculate Minus Directional Index (-DI)
df['minus'] = 100 * talib.SMA(df['minusDM'], timeperiod=len_di) / df['trur']
df['minus'] = np.where(pd.isna(df['minus']), 0, df['minus'])

# Calculate the sum of +DI and -DI
df['sum'] = df['plus'] + df['minus']

# Calculate the Directional Movement Index (ADX)
df['adx'] = 100 * talib.SMA(
    np.abs(df['plus'] - df['minus']) / np.where(df['sum'] == 0, 1, df['sum']),
    timeperiod=lensig
)

# Rename the columns for the output
df = df.rename(columns={'adx': 'Directional Movement Index-1',
                        'plus': 'Directional Movement Index-2',
                        'minus': 'Directional Movement Index-3'})

# Save the updated DataFrame to a CSV file
df.to_csv('data.csv', index=False)
