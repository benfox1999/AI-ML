import pandas as pd
import numpy as np
import talib

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

# Define the TRIX function
def calculate_trix(data, length):
    ema1 = talib.EMA(np.log(data), length)
    ema2 = talib.EMA(ema1, length)
    ema3 = talib.EMA(ema2, length)
    trix = 10000 * (ema3 - ema3.shift(1))
    return trix

# Calculate TRIX and add it as a new column to the DataFrame
df['TRIX'] = calculate_trix(df['close'], length=18)

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)
