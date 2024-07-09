import pandas as pd
import numpy as np

# Load CSV data
df = pd.read_csv('data.csv')

# Convert timestamp strings to datetime objects
df['open_time'] = pd.to_datetime(df['open_time'])
df['close_time'] = pd.to_datetime(df['close_time'])

def calculate_visible_avg_price(src_series, time_series):
  """
  Calculates the visible average price based on the provided source series 
  and time series.

  Args:
    src_series: Pandas Series representing the source data (e.g., 'close').
    time_series: Pandas Series representing the time data (e.g., 'open_time').

  Returns:
    Pandas Series containing the calculated visible average price.
  """
  visible_avg_price = np.nan * np.ones(len(src_series)) 
  for i in range(len(src_series)):
    visible_data = src_series[0:i+1]
    visible_avg_price[i] = visible_data.mean()
  return pd.Series(visible_avg_price)

# Calculate 'Visible Average Price' based on 'close' prices
df['Visible Average Price'] = calculate_visible_avg_price(df['close'], df['open_time'])

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)
