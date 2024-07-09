import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define LSMA function
def calculate_lsma(src, length):
    return talib.LINEARREG(src, length)

# Set LSMA parameters
length = 25
offset = 0

# Calculate LSMA
df['Least Squares Moving Average'] = calculate_lsma(df['close'], length).shift(offset)

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False) 
