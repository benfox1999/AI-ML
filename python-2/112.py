import pandas as pd
import numpy as np
import talib

# Load CSV data 
df = pd.read_csv('data.csv')

# Ensure 'open_time' and other relevant columns are in datetime format
for col in ['open_time', 'close_time']:  # Add other relevant columns here
    if not pd.api.types.is_datetime64_any_dtype(df[col]):
        df[col] = pd.to_datetime(df[col], errors='coerce')

# --- Functions to calculate VWAP and bands ---

def calculate_vwap(df, anchor='Session', src_col='close'):
    """Calculates VWAP based on the given anchor."""

    df['isNewPeriod'] = False
    if anchor == 'Session':
        df['isNewPeriod'] = df['open_time'].dt.date.diff() != pd.Timedelta(days=0)
    # Add other anchor conditions as needed (Week, Month, etc.)

    df['pv'] = df[src_col] * df['volume']
    df['vwap_cumsum'] = df.groupby(df['isNewPeriod'].cumsum())['pv'].cumsum()
    df['volume_cumsum'] = df.groupby(df['isNewPeriod'].cumsum())['volume'].cumsum()
    df['VWAP'] = df['vwap_cumsum'] / df['volume_cumsum']
    df.drop(['pv', 'vwap_cumsum', 'volume_cumsum', 'isNewPeriod'], axis=1, inplace=True)
    return df


def calculate_bands(df, vwap_col='VWAP', mult=1.0, calc_mode='Standard Deviation'):
    """Calculates upper and lower bands."""
    if calc_mode == 'Standard Deviation':
        df['stdev'] = df['close'].rolling(window=len(df)).std()
        band_basis = df['stdev']
    else:  # calc_mode == 'Percentage'
        band_basis = df[vwap_col] * 0.01

    df[f'Upper Band {mult}'] = df[vwap_col] + band_basis * mult
    df[f'Lower Band {mult}'] = df[vwap_col] - band_basis * mult
    df.drop('stdev', axis=1, inplace=True)
    return df

# --- Applying calculations ---

# Parameters from Pine Script input (modify as needed)
hideonDWM = False
anchor = 'Session'
src_col = 'close'  
offset = 0
calc_mode = 'Standard Deviation'
band_multipliers = [1.0, 2.0, 3.0]

# Calculate VWAP
df = calculate_vwap(df, anchor=anchor, src_col=src_col)

# Calculate bands
for mult in band_multipliers:
    df = calculate_bands(df, vwap_col='VWAP', mult=mult, calc_mode=calc_mode)

# Save updated data to CSV
df.to_csv('data.csv', index=False)  # Save to a new file to avoid overwriting
