import pandas as pd
import numpy as np
import talib

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('data.csv')

# Define the Pine Script constants and variables
periods = 30
span_constant = 25

# Calculate the required technical indicators
df['highest_high'] = df['high'].rolling(window=periods).max()
df['lowest_low'] = df['low'].rolling(window=periods).min()
df['span'] = span_constant / (df['highest_high'] - df['lowest_low']) * df['lowest_low']
df['ema34'] = talib.EMA(df['close'], timeperiod=34)
df['avg'] = talib.WCLPRICE(df['high'], df['low'], df['close'])  # Approximation for hlc3

# Calculate the angle of the EMA34
df['y2_ema34'] = (df['ema34'].shift(1) - df['ema34']) / df['avg'] * df['span']
df['c_ema34'] = np.sqrt(1 + df['y2_ema34']**2)
df['emaAngle'] = np.degrees(np.arccos(1 / df['c_ema34'])) * np.sign(df['y2_ema34'])

# Define the conditions for the "Chop Zone" indicator
conditions = [
    (df['emaAngle'] >= 5),
    ((df['emaAngle'] < 5) & (df['emaAngle'] >= 3.57)),
    ((df['emaAngle'] < 3.57) & (df['emaAngle'] >= 2.14)),
    ((df['emaAngle'] < 2.14) & (df['emaAngle'] >= 0.71)),
    (df['emaAngle'] <= -5),
    ((df['emaAngle'] > -5) & (df['emaAngle'] <= -3.57)),
    ((df['emaAngle'] > -3.57) & (df['emaAngle'] <= -2.14)),
    ((df['emaAngle'] > -2.14) & (df['emaAngle'] <= -0.71))
]

# Define the corresponding values for each condition
choices = [
    '#26C6DA',  # colorTurquoise
    '#43A047',  # colorDarkGreen
    '#A5D6A7',  # colorPaleGreen
    '#009688',  # colorLime
    '#D50000',  # colorDarkRed
    '#E91E63',  # colorRed
    '#FF6D00',  # colorOrange
    '#FFB74D'   # colorLightOrange
]

# Apply the conditions and choices to create the "Chop Zone" column
df['Chop Zone'] = np.select(conditions, choices, default='#FDD835')  # colorYellow

# Save the updated DataFrame to a CSV file
df.to_csv('data.csv', index=False)
