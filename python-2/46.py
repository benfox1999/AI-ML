import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define Keltner Channel function
def calculate_keltner_channels(df, length=20, mult=2.0, atrlength=10, bands_style="Average True Range", use_ema=True):
    # Calculate EMA or SMA
    if use_ema:
        df['ma'] = df['close'].ewm(span=length, adjust=False).mean()
    else:
        df['ma'] = df['close'].rolling(window=length).mean()

    # Calculate range
    if bands_style == "True Range":
        df['rangema'] = talib.TRANGE(df['high'], df['low'], df['close'])
    elif bands_style == "Average True Range":
        df['rangema'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=atrlength)
    else:  # Range
        df['rangema'] = (df['high'] - df['low']).rolling(window=length).mean()

    # Calculate upper and lower bands
    df['upper'] = df['ma'] + df['rangema'] * mult
    df['lower'] = df['ma'] - df['rangema'] * mult

    return df

# Apply the function and rename columns
df = calculate_keltner_channels(df)
df.rename(columns={'upper': 'Keltner Channels-1', 'ma': 'Keltner Channels-2', 'lower': 'Keltner Channels-3'}, inplace=True)

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False) 
