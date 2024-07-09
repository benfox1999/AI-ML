import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Convert 'open_time' to datetime objects and set as index
df['open_time'] = pd.to_datetime(df['open_time'], format='%Y-%m-%d %H:%M:%S')

# Set 'open_time' as the index
df.set_index('open_time', inplace=True)


def calculate_multi_time_period_charts(df, timeframe='1D', calculation_method='HLR'):
    """
    Calculates the 'Multi-Time Period Charts' indicator.

    Args:
    df (pd.DataFrame): Input dataframe with OHLCV data.
    timeframe (str): Timeframe for the indicator (e.g., '1D', '4H', '1W').
    calculation_method (str): Method to calculate range ('HLR', 'TR', 'HAR').

    Returns:
    pd.DataFrame: Dataframe with 'Multi-Time Period Charts' column added.
    """

    # Resample dataframe to the specified timeframe
    df_resampled = df.resample(timeframe).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    })

    # Calculate previous close
    df_resampled['prev_close'] = df_resampled['close'].shift(1)

    # Calculate range based on selected method
    if calculation_method == 'HLR':
        df_resampled['top'] = df_resampled['high']
        df_resampled['bottom'] = df_resampled['low']
    elif calculation_method == 'TR':
        df_resampled['top'] = df_resampled[['high', 'prev_close']].max(axis=1)
        df_resampled['bottom'] = df_resampled[['low', 'prev_close']].min(axis=1)
    elif calculation_method == 'HAR':
        df_resampled['ashi_high'] = talib.HT_TRENDLINE(df_resampled['high'])
        df_resampled['ashi_low'] = talib.HT_TRENDLINE(df_resampled['low'])
        df_resampled['top'] = df_resampled['ashi_high']
        df_resampled['bottom'] = df_resampled['ashi_low']

    # Calculate difference for box coloring
    df_resampled['diff'] = df_resampled['close'] - df_resampled['open']

    return df_resampled

# Define parameters
timeframe = '1D'  # Example timeframe, adjust as needed
calculation_method = 'HLR'  # Example calculation method

# Calculate 'Multi-Time Period Charts'
df_with_indicator = calculate_multi_time_period_charts(df.copy(), timeframe, calculation_method)

# Select relevant columns
df_with_indicator = df_with_indicator[['top', 'bottom', 'diff']]

# Rename columns for clarity
df_with_indicator.columns = ['Multi-Time Period Charts-Top', 'Multi-Time Period Charts-Bottom', 'Multi-Time Period Charts-Diff']

# Merge with original dataframe
df = df.join(df_with_indicator, how='left')

# Save the updated dataframe to 'data.csv'
df.to_csv('data.csv')
