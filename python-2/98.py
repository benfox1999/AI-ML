import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Input parameters (matching Pine Script defaults)
long_length = 25
short_length = 13
signal_length = 13

# Calculate True Strength Index (TSI)
def calculate_tsi(data, long_length, short_length):
    close_prices = data['close']
    price_change = close_prices.diff()

    # Double smoothing function
    def double_smooth(src, long_len, short_len):
        first_smooth = talib.EMA(src, timeperiod=long_len)
        return talib.EMA(first_smooth, timeperiod=short_len)

    double_smoothed_pc = double_smooth(price_change, long_length, short_length)
    double_smoothed_abs_pc = double_smooth(np.abs(price_change), long_length, short_length)

    tsi = 100 * (double_smoothed_pc / double_smoothed_abs_pc)
    return tsi

df['True Strength Index-1'] = calculate_tsi(df, long_length, short_length)
df['True Strength Index-2'] = talib.EMA(df['True Strength Index-1'], timeperiod=signal_length)

# Save the updated DataFrame to 'data.csv'
df.to_csv('data.csv', index=False)
