import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define MA calculation function
def calculate_ma(data, type, length):
    """Calculates various moving averages based on the given type."""
    if type == "SMA":
        return talib.SMA(data, length)
    elif type == "EMA":
        return talib.EMA(data, length)
    elif type == "SMMA (RMA)":
        return talib.RMA(data, length)
    elif type == "HullMA":
        return talib.WMA(2 * talib.WMA(data, length // 2) - talib.WMA(data, length), int(np.sqrt(length)))
    elif type == "WMA":
        return talib.WMA(data, length)
    elif type == "VWMA":
        return talib.VWMA(data, length)
    elif type == "DEMA":
        ema1 = talib.EMA(data, length)
        ema2 = talib.EMA(ema1, length)
        return 2 * ema1 - ema2
    elif type == "TEMA":
        ema1 = talib.EMA(data, length)
        ema2 = talib.EMA(ema1, length)
        ema3 = talib.EMA(ema2, length)
        return (3 * ema1) - (3 * ema2) + ema3
    else:
        return np.nan

# Set parameters
ma_type = "TEMA"  # Example: "TEMA"
ma_length = 50
trend_duration = 20

# Calculate MA
df['ma'] = calculate_ma(df['close'], ma_type, ma_length)

# Determine falling and rising conditions
df['falling'] = df['ma'].rolling(window=trend_duration).apply(lambda x: all(x[i] > x[i + 1] for i in range(len(x) - 1)), raw=True)
df['rising'] = df['ma'].rolling(window=trend_duration).apply(lambda x: all(x[i] < x[i + 1] for i in range(len(x) - 1)), raw=True)

# Identify buy and sell signals
df['MA Sabres [LuxAlgo]-buy'] = (df['falling'].shift(1).astype(bool) & (df['ma'] > df['ma'].shift(1))).astype(int)
df['MA Sabres [LuxAlgo]-sell'] = (df['rising'].shift(1).astype(bool) & (df['ma'] < df['ma'].shift(1))).astype(int)



# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)
