import pandas as pd
import numpy as np
import talib

# Load data from CSV
df = pd.read_csv("data.csv")

# Stochastic Oscillator Parameters
periodK = 14
smoothK = 1
periodD = 3

# Calculate %K and %D using talib.STOCH (and unpacking results)
slowk, fastk = talib.STOCH(df['high'], df['low'], df['close'], fastk_period=periodK, slowk_period=periodD, slowd_period=smoothK)

df['%K'] = fastk  # Directly assign fastk to the %K column
df['%D'] = slowk  # Directly assign slowk to the %D column (smoothing already done)

# Save the updated DataFrame to the CSV
df.to_csv("data.csv", index=False)
