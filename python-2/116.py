import pandas as pd
import numpy as np

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('data.csv')

def calculate_fractals(df, n=2):
    """
    Calculates Williams Fractals for a given DataFrame.

    Args:
        df (pd.DataFrame): DataFrame with 'high' and 'low' columns.
        n (int, optional): Number of periods. Defaults to 2.

    Returns:
        pd.DataFrame: DataFrame with 'upFractal' and 'downFractal' columns added.
    """

    # UpFractal
    df['upFractal'] = np.where((
        (df['high'].rolling(n).max().shift(n) < df['high']) &
        ((df['high'].rolling(n).max().shift(-n) < df['high']) |
         (df['high'].rolling(n + 1).max().shift(-n - 1) < df['high']) |
         (df['high'].rolling(n + 2).max().shift(-n - 2) < df['high']) |
         (df['high'].rolling(n + 3).max().shift(-n - 3) < df['high']) |
         (df['high'].rolling(n + 4).max().shift(-n - 4) < df['high']))
    ), df['high'], np.nan)

    # downFractal
    df['downFractal'] = np.where((
        (df['low'].rolling(n).min().shift(n) > df['low']) &
        ((df['low'].rolling(n).min().shift(-n) > df['low']) |
         (df['low'].rolling(n + 1).min().shift(-n - 1) > df['low']) |
         (df['low'].rolling(n + 2).min().shift(-n - 2) > df['low']) |
         (df['low'].rolling(n + 3).min().shift(-n - 3) > df['low']) |
         (df['low'].rolling(n + 4).min().shift(-n - 4) > df['low']))
    ), df['low'], np.nan)

    return df

# Calculate the fractals with a period of 2 (default)
df = calculate_fractals(df, n=2)

# Save the updated DataFrame back to the CSV file
df.to_csv('data.csv', index=False)
