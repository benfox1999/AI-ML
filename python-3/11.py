import pandas as pd
import numpy as np
import talib

# Load the CSV data
df = pd.read_csv('data.csv')

# Convert 'open_time' and 'close_time' to datetime objects
df['open_time'] = pd.to_datetime(df['open_time'])
df['close_time'] = pd.to_datetime(df['close_time'])

# Constants (Matching Pine Script input)
HOURLY = 'HOURLY'
DAILY = 'DAILY'
WEEKLY = 'WEEKLY'
MONTHLY = 'MONTHLY'

ANCHORING_PERIOD = DAILY  # Choose from: HOURLY, DAILY, WEEKLY, MONTHLY
BAR_WIDTH = 2 

# Function to determine buy and sell volume
def get_volume_type(row):
    if row['close'] > row['open']:
        return 'buy'
    elif row['close'] < row['open']:
        return 'sell'
    else:
        return 'ignore' 

df['volume_type'] = df.apply(get_volume_type, axis=1)

# Function to calculate buy and sell volume for different periods
def calculate_periodic_volume(df, period):
    if period == HOURLY:
        df['hour'] = df['open_time'].dt.hour
        group_cols = ['hour'] 
    elif period == DAILY:
        df['day'] = df['open_time'].dt.day
        group_cols = ['day']
    elif period == WEEKLY:
        df['week'] = df['open_time'].dt.isocalendar().week
        group_cols = ['week']
    elif period == MONTHLY:
        df['month'] = df['open_time'].dt.month
        group_cols = ['month']
    else:
        raise ValueError("Invalid period specified.")

    buy_volume = (
        df[df['volume_type'] == 'buy']
        .groupby(group_cols)['volume']
        .sum()
        .reset_index()
    )
    sell_volume = (
        df[df['volume_type'] == 'sell']
        .groupby(group_cols)['volume']
        .sum()
        .reset_index()
    )

    return buy_volume, sell_volume

# Calculate buy and sell volume based on ANCHORING_PERIOD
buy_volume, sell_volume = calculate_periodic_volume(df.copy(), ANCHORING_PERIOD)

# Rename columns in the results
buy_volume.columns = ['day', 'Periodic Activity Tracker [LuxAlgo]-buy']  
sell_volume.columns = ['day', 'Periodic Activity Tracker [LuxAlgo]-sell']

#Add time period column to original dataframe
df['day'] = df['open_time'].dt.day

# Add new columns to the DataFrame using a merge
df = df.merge(buy_volume, on='day', how='left')
df = df.merge(sell_volume, on='day', how='left')

# Fill missing values (e.g., fill with zeros)
df[['Periodic Activity Tracker [LuxAlgo]-buy', 'Periodic Activity Tracker [LuxAlgo]-sell']] = df[['Periodic Activity Tracker [LuxAlgo]-buy', 'Periodic Activity Tracker [LuxAlgo]-sell']].fillna(0)

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)
