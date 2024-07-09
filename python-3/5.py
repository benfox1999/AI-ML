import pandas as pd

# Load the CSV data
df = pd.read_csv('data.csv')

# Convert timestamp columns to datetime objects if they are not already
df['open_time'] = pd.to_datetime(df['open_time'])
df['close_time'] = pd.to_datetime(df['close_time'])


def calculate_volume_activity(df, symbol, timeframe='1D'):
    """
    Calculates buy and sell volume activity based on the provided timeframe.

    Args:
        df (pd.DataFrame): DataFrame containing OHLCV data.
        symbol (str): The trading symbol (e.g., 'BTCUSDT').
        timeframe (str, optional): The timeframe for analysis. Defaults to '1D'.

    Returns:
        pd.DataFrame: DataFrame with columns for buy and sell volume, named after the symbol.
    """

    # Resample data to the specified timeframe (default is daily)
    df_resampled = df.resample(timeframe, on='open_time').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    })

    # Calculate buy and sell volume
    df_resampled[f'{symbol}_buy'] = ((df_resampled['close'] - df_resampled['low']) / (df_resampled['high'] - df_resampled['low'])) * df_resampled['volume']
    df_resampled[f'{symbol}_sell'] = ((df_resampled['high'] - df_resampled['close']) / (df_resampled['high'] - df_resampled['low'])) * df_resampled['volume']

    return df_resampled[[f'{symbol}_buy', f'{symbol}_sell']]


# Symbols from the Pine Script
symbols = [
    'BTCUSDT'
]

# Calculate and merge volume activity for each symbol
volume_dfs = []
for symbol in symbols:
    volume_data = calculate_volume_activity(df, symbol)
    volume_dfs.append(volume_data)

# Merge all volume DataFrames into the original DataFrame
df_updated = pd.merge(df, pd.concat(volume_dfs), on='open_time', how='left')

# Handle NaN values (e.g., fill with zeros)
df_updated.fillna(0, inplace=True)

# Save the updated DataFrame to a new CSV
df_updated.to_csv('data.csv', index=False)
