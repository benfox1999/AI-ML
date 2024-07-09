import pandas as pd
import numpy as np
import talib

# Load CSV into a Pandas DataFrame
df = pd.read_csv('data.csv')

length = 60  # Percent Rank Length

def calculate_percent_rank(close_prices):
    """Calculates the percent rank for a given series of close prices."""
    # TA-Lib equivalent for PERCENTRANK is MOM (Momentum)
    momentum = talib.MOM(close_prices, timeperiod=length)

    # Normalize momentum to 0-100 scale (approximation of percent rank)
    min_mom = momentum.min()
    max_mom = momentum.max()
    percent_rank = ((momentum - min_mom) / (max_mom - min_mom)) * 100

    return percent_rank

# Calculate percent rank for each symbol
df['CRYPTOCAP:TOTAL'] = calculate_percent_rank(df['close'])
df['BTCUSD'] = calculate_percent_rank(df['close'])

# Save the updated DataFrame back to CSV
df.to_csv('data.csv', index=False)
