import pandas as pd
import numpy as np

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

# Convert 'open_time' and 'close_time' columns to datetime objects if needed
df['open_time'] = pd.to_datetime(df['open_time'])
df['close_time'] = pd.to_datetime(df['close_time'])

def visible_average_price(df, source_column='close'):
    """
    Calculates the Visible Average Price based on the provided source column.

    Args:
        df (pd.DataFrame): The input DataFrame.
        source_column (str): The column to use as the source for the calculation.

    Returns:
        pd.Series: A Series containing the calculated Visible Average Price.
    """
    src_vals = []
    avg_prices = []
    for i in range(len(df)):
        src_vals.insert(0, df[source_column].iloc[i])
        avg_prices.append(np.mean(src_vals))
    return pd.Series(avg_prices)

# Calculate the 'Visible Average Price' and add it as a new column
df['Visible Average Price'] = visible_average_price(df, source_column='close')

# Save the modified DataFrame back to the CSV file
df.to_csv('data.csv', index=False)
