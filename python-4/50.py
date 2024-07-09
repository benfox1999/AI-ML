import pandas as pd
import numpy as np
import talib

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

# Functions
def is_up(df, index):
    return df['close'][index] > df['open'][index]

def is_down(df, index):
    return df['close'][index] < df['open'][index]

def is_ob_up(df, index):
    return is_down(df, index + 1) and is_up(df, index) and df['close'][index] > df['high'][index + 1]

def is_ob_down(df, index):
    return is_up(df, index + 1) and is_down(df, index) and df['close'][index] < df['low'][index + 1]

def is_fvg_up(df, index):
    return df['low'][index] > df['high'][index + 2]

def is_fvg_down(df, index):
    return df['high'][index] < df['low'][index + 2]

#  Pivots 
pivot_lookup = 1  # Default value from Pine Script input
hvb_ema_period = 12  
hvb_multiplier = 1.5  
def is_pivot_high(highs, lows, i, length):
    """Checks if index i is a pivot high within a window of length."""
    if i < length or i >= len(highs) - length:
        return False
    return highs[i] > highs[i - length:i + length + 1].max()

def is_pivot_low(highs, lows, i, length):
    """Checks if index i is a pivot low within a window of length."""
    if i < length or i >= len(lows) - length:
        return False
    return lows[i] < lows[i - length:i + length + 1].min()


# Pivots 
df['hih'] = np.nan
df['lol'] = np.nan
for i in range(len(df)):
    if is_pivot_high(df['high'].values, df['low'].values, i, pivot_lookup):
        df.loc[i, 'hih'] = df['high'][i]
    if is_pivot_low(df['high'].values, df['low'].values, i, pivot_lookup):
        df.loc[i, 'lol'] = df['low'][i]

df['top'] = np.where(df['hih'] > 0, df['high'].shift(-pivot_lookup), np.nan)
df['bottom'] = np.where(df['lol'] > 0, df['low'].shift(-pivot_lookup), np.nan)


# Order Block 
df['Super OrderBlock / FVG / BoS Tools by makuchaku & eFe-buy'] = np.where(is_ob_up(df, 1), 1, 0)
df['Super OrderBlock / FVG / BoS Tools by makuchaku & eFe-sell'] = np.where(is_ob_down(df, 1), 1, 0)

# Fair Value Gap 
df['Super OrderBlock / FVG / BoS Tools by makuchaku & eFe-buy'] = np.where(is_fvg_up(df, 0), 1,
                                                                            df['Super OrderBlock / FVG / BoS Tools by makuchaku & eFe-buy'])
df['Super OrderBlock / FVG / BoS Tools by makuchaku & eFe-sell'] = np.where(is_fvg_down(df, 0), 1,
                                                                            df['Super OrderBlock / FVG / BoS Tools by makuchaku & eFe-sell'])

# Rejection Block (RJB) logic requires iterating through the DataFrame with state preservation.
# This cannot be easily vectorized with Pandas. 
#  - Implement the RJB logic using a loop and state variables
#  - Create columns for RJB signals: 'Super OrderBlock / FVG / BoS Tools by makuchaku & eFe-buy' and 'Super OrderBlock / FVG / BoS Tools by makuchaku & eFe-sell'

# Crossovers (Break of Structure - BOS)
def crossover(series1, series2):
    """
    Detects crossovers (series1 crossing above series2) and crossunders (series1 crossing below series2).
    """
    cross_over = (series1 > series2) & (series1.shift(1) <= series2.shift(1))
    cross_under = (series1 < series2) & (series1.shift(1) >= series2.shift(1))
    return cross_over, cross_under  # Return two boolean Series

# --- Pivots ---
# ... (Your pivot calculation logic)

# --- Order Block, FVG ---
# ... (Your logic for order blocks and FVGs)

# --- Crossovers (Break of Structure - BOS) ---
crossover_top, _ = crossover(df['close'], df['top'])  # Ignore crossunder here
_, crossunder_bottom = crossover(df['close'], df['bottom'])  # Ignore crossover here

df['Super OrderBlock / FVG / BoS Tools by makuchaku & eFe-buy'] = np.where(
    crossover_top, 1, df['Super OrderBlock / FVG / BoS Tools by makuchaku & eFe-buy']
)
df['Super OrderBlock / FVG / BoS Tools by makuchaku & eFe-sell'] = np.where(
    crossunder_bottom, 1, df['Super OrderBlock / FVG / BoS Tools by makuchaku & eFe-sell']
)


# Premium Premium & Discount Discount (PPDD) logic 
# - Requires iterating through the DataFrame with state preservation
# - Implement the PPDD logic using a loop and state variables
# - Create columns for PPDD signals: 'Super OrderBlock / FVG / BoS Tools by makuchaku & eFe-buy' and 'Super OrderBlock / FVG / BoS Tools by makuchaku & eFe-sell'

# High Volume Bar (HVB)
hvb_ema_period = 12  # Default value from Pine Script input
hvb_multiplier = 1.5  # Default value from Pine Script input

df['volume_ema'] = talib.EMA(df['volume'], timeperiod=hvb_ema_period)
df['is_high_volume'] = df['volume'] > (hvb_multiplier * df['volume_ema'])

df['Super OrderBlock / FVG / BoS Tools by makuchaku & eFe-buy'] = np.where((is_up(df, 0)) &
                                                                            (df['is_high_volume']), 1,
                                                                            df['Super OrderBlock / FVG / BoS Tools by makuchaku & eFe-buy'])
df['Super OrderBlock / FVG / BoS Tools by makuchaku & eFe-sell'] = np.where((is_down(df, 0)) &
                                                                            (df['is_high_volume']), 1,
                                                                            df['Super OrderBlock / FVG / BoS Tools by makuchaku & eFe-sell'])

# Stacked OB + FVG logic
# - Requires iterating through the DataFrame with state preservation
# - Implement the Stacked OB + FVG logic using a loop and state variables
# - Create columns for Stacked OB + FVG signals: 'Super OrderBlock / FVG / BoS Tools by makuchaku & eFe-buy' and 'Super OrderBlock / FVG / BoS Tools by makuchaku & eFe-sell'

# Save the updated DataFrame to a CSV file (optional)
# df.to_csv('data_updated.csv', index=False)
