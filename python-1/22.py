import pandas as pd
import numpy as np
import talib

# Load data from CSV
data = pd.read_csv("data.csv")

# Define Supertrend function
def supertrend(df, atr_period=10, factor=3.0):
    high = df["high"]
    low = df["low"]
    close = df["close"]

    # Calculate ATR
    atr = talib.ATR(high, low, close, timeperiod=atr_period)

    # Calculate Supertrend
    up = close - (factor * atr)
    down = close + (factor * atr)

    # Initialize trend and direction
    trend = np.zeros_like(close)
    direction = np.zeros_like(close)
    trend[0] = up[0] if close[0] > up[0] else down[0]
    direction[0] = 1 if close[0] > up[0] else -1

    # Iterate through data to determine trend and direction
    for i in range(1, len(close)):
        if direction[i - 1] == 1:
            trend[i] = max(up[i], trend[i - 1])
        else:
            trend[i] = min(down[i], trend[i - 1])
        direction[i] = 1 if close[i] > trend[i] else -1

    return trend, direction


# Calculate Supertrend
data["Supertrend"], data["Supertrend Direction"] = supertrend(data)

# Generate buy/sell signals based on direction changes
data["Supertrend-buy"] = np.where(data["Supertrend Direction"].diff() < 0, 1, 0)
data["Supertrend-sell"] = np.where(data["Supertrend Direction"].diff() > 0, 1, 0)

# Save the updated DataFrame to the same CSV file
data.to_csv("data.csv", index=False)

