import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Settings (matching Pine Script inputs)
length = 10
offset = 0
ma_type_input = "SMA"  
ma_length_input = 14
bb_mult_input = 2.0

# Calculate RVI
df['stddev'] = df['close'].rolling(window=length).std()

# Calculate Upper and Lower RVI
df['upper'] = np.where(df['close'].diff() <= 0, 0, df['stddev'])
df['lower'] = np.where(df['close'].diff() > 0, 0, df['stddev'])
df['upper'] = df['upper'].ewm(alpha=1/length, adjust=False).mean()
df['lower'] = df['lower'].ewm(alpha=1/length, adjust=False).mean()

df['Relative Volatility Index'] = (df['upper'] / (df['upper'] + df['lower']) * 100)

# Function to calculate different moving averages
def calculate_ma(source, length, type):
    if type == "SMA":
        return talib.SMA(source, length) 
    elif type == "Bollinger Bands":
        upper, middle, lower = talib.BBANDS(source, length, bb_mult_input)
        return middle, upper, lower
    elif type == "EMA":
        return talib.EMA(source, length)
    elif type == "SMMA (RMA)":
        return talib.RMA(source, length)
    elif type == "WMA":
        return talib.WMA(source, length)
    elif type == "VWMA":
        return talib.VWMA(source, length)

# Calculate RVI-based MA and Bollinger Bands
if ma_type_input == "Bollinger Bands":
    df['Relative Volatility Index-1'], df['Upper Bollinger Band'], df['Lower Bollinger Band'] = calculate_ma(
        df['Relative Volatility Index'], ma_length_input, ma_type_input
    )
else:
    df['Relative Volatility Index-1'] = calculate_ma(
        df['Relative Volatility Index'], ma_length_input, ma_type_input
    )

# Handle offset (not applicable to CSV output, adjust indexing if needed)
df['Relative Volatility Index'] = df['Relative Volatility Index'].shift(offset)
df['Relative Volatility Index-1'] = df['Relative Volatility Index-1'].shift(offset)
if ma_type_input == "Bollinger Bands":
    df['Upper Bollinger Band'] = df['Upper Bollinger Band'].shift(offset)
    df['Lower Bollinger Band'] = df['Lower Bollinger Band'].shift(offset)

# Save updated DataFrame to CSV
df.to_csv('data.csv', index=False)
