import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Convert timestamps to datetime objects if needed
df['open_time'] = pd.to_datetime(df['open_time'])

# Define Pine Script input parameters
prd = 5
source = 'Close'  # or 'High/Low'
searchdiv = 'Regular'  # or 'Hidden', 'Regular/Hidden'
showlimit = 1
maxpp = 10
maxbars = 100
dontconfirm = False
calcmom = True

# Calculate indicators
df['rsi'] = talib.RSI(df['close'], timeperiod=14)
df['macd'], df['macdsignal'], df['macdhist'] = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
df['mom'] = talib.MOM(df['close'], timeperiod=10)

# Function to find pivot points
def find_pivots(df, prd, source):
    ph = np.zeros(len(df))
    pl = np.zeros(len(df))

    for i in range(prd, len(df) - prd):
        if source == 'Close':
            pivot_high = df['close'][i - prd:i + prd + 1].max()
            pivot_low = df['close'][i - prd:i + prd + 1].min()
        else:  # source == 'High/Low'
            pivot_high = df['high'][i - prd:i + prd + 1].max()
            pivot_low = df['low'][i - prd:i + prd + 1].min()

        if df['close'][i] == pivot_high:
            ph[i] = 1
        if df['close'][i] == pivot_low:
            pl[i] = 1

    return ph, pl

df['ph'], df['pl'] = find_pivots(df, prd, source)

# Function to check for divergence
def check_divergence(df, indicator_col, ph_col, pl_col, maxpp, maxbars, dontconfirm, searchdiv, positive_div=True):
    divergence = np.zeros(len(df))

    for i in range(maxbars, len(df)):
        if (positive_div and df[ph_col][i] == 1) or (not positive_div and df[pl_col][i] == 1):
            for j in range(1, min(maxpp, i) + 1):
                if (positive_div and df[pl_col][i - j] == 1) or (not positive_div and df[ph_col][i - j] == 1):
                    if (positive_div and df[indicator_col][i] < df[indicator_col][i - j] and df['close'][i] > df['close'][i - j]) or \
                       (not positive_div and df[indicator_col][i] > df[indicator_col][i - j] and df['close'][i] < df['close'][i - j]):
                        divergence[i] = 1
                        break

    return divergence

# Check for divergence in selected indicators
if calcmom:
    df['Divergence for Many Indicators v4'] = check_divergence(df, 'mom', 'ph', 'pl', maxpp, maxbars, dontconfirm, searchdiv, positive_div=True)

# Save the results to CSV
df.to_csv('data.csv', index=False)
