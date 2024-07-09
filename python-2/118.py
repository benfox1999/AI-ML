import pandas as pd
import numpy as np

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

# Define the 'n' periods parameter
n = 2  # Default value, adjust as needed

# Function to calculate Williams Fractals
def calculate_williams_fractals(df, n):
    """Calculates Williams Fractals and adds 'upFractal' and 'downFractal' columns to the DataFrame."""

    for i in range(n, len(df)):
        # UpFractal
        upflagDownFrontier = all(df['high'][i - n : i] < df['high'][i])
        upflagUpFrontier = any(
            [
                all(df['high'][i + 1 : i + j + 1] < df['high'][i])
                for j in range(1, min(n, len(df) - i))
            ]
        )
        upFractal = upflagDownFrontier and upflagUpFrontier

        # DownFractal
        downflagDownFrontier = all(df['low'][i - n : i] > df['low'][i])
        downflagUpFrontier = any(
            [
                all(df['low'][i + 1 : i + j + 1] > df['low'][i])
                for j in range(1, min(n, len(df) - i))
            ]
        )
        downFractal = downflagDownFrontier and downflagUpFrontier

        df.loc[i, 'upFractal'] = upFractal
        df.loc[i, 'downFractal'] = downFractal

    return df


# Calculate Williams Fractals and update the DataFrame
df = calculate_williams_fractals(df, n)

# Save the updated DataFrame to a CSV file
df.to_csv('data.csv', index=False)
