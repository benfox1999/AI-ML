import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

def volatility_stop(src, length, factor):
    """
    Calculates the Volatility Stop indicator.

    Args:
        src (pd.Series): Input price series.
        length (int): ATR period.
        factor (float): ATR multiplier.

    Returns:
        pd.DataFrame: DataFrame with 'Volatility Stop' and 'uptrend' columns.
    """
    # Calculate ATR
    df['atr'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=length) * factor

    # Initialize variables (use .copy() to create independent copies)
    df['max'] = src.copy()
    df['min'] = src.copy()
    df['uptrend'] = True
    df['Volatility Stop'] = np.nan

    # Iterate through data using .loc for explicit assignment
    for i in range(1, len(df)):
        df.loc[i, 'max'] = max(df.loc[i-1, 'max'], src.iloc[i])
        df.loc[i, 'min'] = min(df.loc[i-1, 'min'], src.iloc[i])

        if df.loc[i-1, 'uptrend']:
            df.loc[i, 'Volatility Stop'] = max(df.loc[i-1, 'Volatility Stop'], df.loc[i, 'max'] - df.loc[i, 'atr'])
        else:
            df.loc[i, 'Volatility Stop'] = min(df.loc[i-1, 'Volatility Stop'], df.loc[i, 'min'] + df.loc[i, 'atr'])

        df.loc[i, 'uptrend'] = (src.iloc[i] - df.loc[i, 'Volatility Stop']) >= 0.0

        # Trend change detection
        if df.loc[i, 'uptrend'] != df.loc[i-1, 'uptrend']:
            df.loc[i, 'max'] = src.iloc[i]
            df.loc[i, 'min'] = src.iloc[i]

            if df.loc[i, 'uptrend']:
                df.loc[i, 'Volatility Stop'] = df.loc[i, 'max'] - df.loc[i, 'atr']
            else:
                df.loc[i, 'Volatility Stop'] = df.loc[i, 'min'] + df.loc[i, 'atr']

    return df[['Volatility Stop', 'uptrend']]

# Calculate Volatility Stop
df[['Volatility Stop', 'uptrend']] = volatility_stop(df['close'], length=20, factor=2.0)

# Save updated DataFrame to CSV
df.to_csv('data.csv', index=False)
