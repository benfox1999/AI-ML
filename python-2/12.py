import pandas as pd
import numpy as np
import talib as ta

# Load the CSV data
df = pd.read_csv('data.csv')

# Define the ADR calculation function
def calculate_adr(df, length):
  df['Average Day Range'] = ta.SMA(df['high'] - df['low'], timeperiod=length)
  return df

# Set the ADR length
lengthInput = 14

# Calculate ADR and append to the DataFrame
df = calculate_adr(df, lengthInput)

# Save the updated DataFrame back to CSV
df.to_csv('data.csv', index=False) 
