import pandas as pd
import numpy as np
import talib

# Load the CSV file into a Pandas DataFrame
data = pd.read_csv("data.csv")

# Calculate the Chaikin Oscillator
def chaikin_oscillator(data, short_period, long_period):
    """
    Calculates the Chaikin Oscillator.

    Args:
        data: Pandas DataFrame with 'high', 'low', 'close', and 'volume' columns.
        short_period: Short moving average period.
        long_period: Long moving average period.

    Returns:
        Pandas Series with the Chaikin Oscillator values.
    """
    data['ADL'] = (
        ((data['close'] - data['low']) - (data['high'] - data['close'])) /
        (data['high'] - data['low']) * data['volume']
    )
    data['ADL'].fillna(0, inplace=True)  # Replace potential NaN values with 0
    data['Chaikin Oscillator'] = talib.EMA(data['ADL'], timeperiod=short_period) - talib.EMA(data['ADL'], timeperiod=long_period)
    return data['Chaikin Oscillator']

# Set the input parameters
short_period = 3
long_period = 10

# Calculate the Chaikin Oscillator and add it as a new column to the DataFrame
data['Chaikin Oscillator'] = chaikin_oscillator(data.copy(), short_period, long_period)

# Save the updated DataFrame to a CSV file
data.to_csv("data.csv", index=False)
