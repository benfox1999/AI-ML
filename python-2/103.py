import pandas as pd
import numpy as np

# Load the CSV data
df = pd.read_csv('data.csv')

# Convert timestamps if necessary
# Assuming 'open_time' and 'close_time' are Unix timestamps
df['open_time'] = pd.to_datetime(df['open_time'])
df['close_time'] = pd.to_datetime(df['close_time'])

def calculate_visible_average_price(df, src_col='close'):
    """
    Calculates the Visible Average Price based on the provided source column.

    Args:
        df (pd.DataFrame): The input DataFrame.
        src_col (str, optional): The source column for calculation. Defaults to 'close'.

    Returns:
        pd.DataFrame: DataFrame with the 'Visible Average Price' column added.
    """

    df['Visible Average Price'] = np.nan  # Initialize the column with NaN values

    for i in range(len(df)):
        # Simulate Pine Script's visible bar range
        visible_start = i
        visible_end = len(df) - 1 

        # Extract visible values from the source column
        src_vals = df[src_col].iloc[visible_start:visible_end + 1].values

        # Calculate and store the average
        df.loc[df.index[i], 'Visible Average Price'] = np.mean(src_vals)

    return df

# Calculate the indicator
df = calculate_visible_average_price(df)

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)
