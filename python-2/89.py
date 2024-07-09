import pandas as pd
import numpy as np
import talib

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('data.csv')

# Define the input parameters
lengthK = 10
lengthD = 3
lengthEMA = 3

# Calculate the EMA of the EMA (Double EMA)
def emaEma(source, length):
    return talib.EMA(talib.EMA(source, length), length)

# Calculate the Stochastic Momentum Index (SMI)
df['highestHigh'] = df['high'].rolling(window=lengthK).max()
df['lowestLow'] = df['low'].rolling(window=lengthK).min()
df['highestLowestRange'] = df['highestHigh'] - df['lowestLow']
df['relativeRange'] = df['close'] - (df['highestHigh'] + df['lowestLow']) / 2
df['SMI'] = 200 * (emaEma(df['relativeRange'], lengthD) / emaEma(df['highestLowestRange'], lengthD))

# Calculate the SMI-based EMA
df['SMI-based EMA'] = talib.EMA(df['SMI'], lengthEMA)

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)
