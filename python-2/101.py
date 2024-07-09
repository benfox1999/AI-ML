import pandas as pd
import numpy as np

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

# Convert the 'time' column to datetime objects if it's not already
df['open_time'] = pd.to_datetime(df['open_time'])

# Create a new column for the 'Visible Average Price'
df['Visible Average Price'] = np.nan

# Iterate over the DataFrame rows
for i in range(len(df)):
    # Determine the visible range
    time_left = df['open_time'].iloc[max(0, i - 100000)]
    time_right = df['open_time'].iloc[i]

    # Filter the DataFrame for the visible range
    visible_df = df[(df['open_time'] >= time_left) & (df['open_time'] <= time_right)]

    # Calculate the average of the 'close' column in the visible range
    df.loc[i, 'Visible Average Price'] = visible_df['close'].mean()

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)
