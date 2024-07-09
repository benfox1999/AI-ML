import pandas as pd
import numpy as np
import talib

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

def calculate_aroon(df, length=14):
  """Calculates Aroon Up and Aroon Down indicators.

  Args:
    df: Pandas DataFrame with 'high' and 'low' columns.
    length: Lookback period for Aroon calculation.

  Returns:
    Pandas DataFrame with 'Aroon-1' and 'Aroon-2' columns added.
  """

  df['Aroon-1'] = 100 * (length - df['high'].rolling(length + 1).apply(lambda x: x[::-1].argmax(), raw=True)) / length
  df['Aroon-2'] = 100 * (length - df['low'].rolling(length + 1).apply(lambda x: x[::-1].argmin(), raw=True)) / length
  return df

# Calculate Aroon indicators with a length of 14
df = calculate_aroon(df, length=14)

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)
