import pandas as pd
import numpy as np
import talib

# Load data from CSV
df = pd.read_csv('data.csv')

# Convert 'open_time' and 'close_time' to datetime objects (assuming they are in a standard format)
df['open_time'] = pd.to_datetime(df['open_time'])
df['close_time'] = pd.to_datetime(df['close_time'])

# --- Input Parameters (mimicking Pine Script inputs) ---
start_year = 2015
cutoff_percent = 10
skipped_months_str = "2023-03, 2024-01"  # Example: Skip March 2023 and January 2024

# Create a list of ignored months (YYYYMM format)
ignored_months = [int(m.replace('-', '')) for m in skipped_months_str.split(', ')]

# --- Helper Functions ---
def change_percent(source):
    """Calculates the one-bar change percentage."""
    return 100.0 * (source - source.shift(1)) / source.shift(1)

def calculate_monthly_changes(df, start_year):
    """Calculates monthly price change percentages."""
    df['Year'] = df['open_time'].dt.year
    df['Month'] = df['open_time'].dt.month

    # Filter data starting from the specified year
    df_filtered = df[df['Year'] >= start_year].copy()

    # Calculate monthly price change percentages
    df_filtered['Monthly_Change'] = df_filtered.groupby(['Year', 'Month'])['close'].transform(change_percent)

    return df_filtered[['Year', 'Month', 'Monthly_Change']]

# --- Main Calculations ---

# 1. Calculate Monthly Changes
monthly_changes_df = calculate_monthly_changes(df.copy(), start_year)

# 2. Create a matrix to store monthly changes (excluding skipped months)
changes_matrix = monthly_changes_df.pivot_table(
    values='Monthly_Change', index='Year', columns='Month'
).fillna(0)  # Fill NaN with 0 (adjust if needed)

# 3. Calculate Expected Price, Average, and Standard Deviation
df['Year'] = df['open_time'].dt.year
df['Month'] = df['open_time'].dt.month

df['Expected_Price'] = np.nan
df['Historical_Avg'] = np.nan
df['Historical_StDev'] = np.nan

for index, row in df.iterrows():
    curr_year, curr_month = row['Year'], row['Month']

    if curr_year >= start_year and int(f"{curr_year:04}{curr_month:02}") not in ignored_months:
        try:
            curr_month_avg = changes_matrix.loc[curr_year, curr_month]
            curr_month_stdev = changes_matrix.loc[:, curr_month].std()
            df.loc[index, 'Expected_Price'] = df.loc[index - 1, 'close'] + (df.loc[index - 1, 'close'] * curr_month_avg / 100)
            df.loc[index, 'Historical_Avg'] = curr_month_avg
            df.loc[index, 'Historical_StDev'] = curr_month_stdev
        except KeyError:
            # Handle cases where the year/month combination is not in changes_matrix
            df.loc[index, 'Expected_Price'] = np.nan
            df.loc[index, 'Historical_Avg'] = np.nan
            df.loc[index, 'Historical_StDev'] = np.nan


# --- Save the results back to the CSV ---
df.to_csv('data.csv', index=False)
