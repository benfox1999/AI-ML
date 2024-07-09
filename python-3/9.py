import pandas as pd
import numpy as np
import talib

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('data.csv')

# Convert the 'open_time' and 'close_time' columns to datetime objects
df['open_time'] = pd.to_datetime(df['open_time'])
df['close_time'] = pd.to_datetime(df['close_time'])

# Set 'open_time' as the DataFrame index
df.set_index('open_time', inplace=True)

# Infer frequency from the datetime index
inferred_freq = pd.infer_freq(df.index)

# Fill missing values if frequency is inferred
if inferred_freq is not None:
    df = df.asfreq(inferred_freq)
    
# --- User Inputs (mimic Pine Script inputs) ---
repaint_input = False
source_column = 'close'
htf_selection = 'Multiple of chart TF'
fixed_higher_timeframe = '1D'
timeframe_multiple = 4


# --- Function to get higher timeframe data ---
def get_htf_data(data, tf, column, repaint=False):
    """
    Simulates Pine Script's request.security functionality for higher timeframe data.

    Args:
        data (pd.DataFrame): Input DataFrame with 'open', 'high', 'low', 'close' columns.
        tf (str): Higher timeframe string (e.g., '1D', '4H').
        column (str): Column name to retrieve from the higher timeframe.
        repaint (bool): If True, allows repainting (accesses current bar data).
                      If False, prevents repainting (uses last confirmed bar data).

    Returns:
        pd.Series: Higher timeframe data.
    """
    
    # Resample to the higher timeframe
    htf_data = data.resample(tf).agg(
        {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'}
    )
    
    if not repaint:
        # Shift the data to avoid repainting
        htf_data = htf_data.shift(1)
    
    return htf_data[column]

# Determine the requested higher timeframe
if htf_selection == 'Fixed TF':
    requested_tf = fixed_higher_timeframe
elif htf_selection == 'Multiple of chart TF':
    if df.index.freq is None:
        print("Error: Frequency could not be inferred. Please ensure the data is regular.")
    else:
        if df.index.freq == 'T':
            requested_tf = f'{timeframe_multiple}T'
        else:
            requested_tf = df.index.freq * timeframe_multiple

# Get higher timeframe data for the specified source column
df['htf_data'] = get_htf_data(df, requested_tf, source_column, repaint=repaint_input)

# --- Example: Apply calculations based on htf_data (replace with your logic) ---
# Example: Calculate a simple moving average (SMA) on the higher timeframe data
df['htf_sma'] = talib.SMA(df['htf_data'], timeperiod=5)

# --- Save the results ---
df.to_csv('data.csv')
