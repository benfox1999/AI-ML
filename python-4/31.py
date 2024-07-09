import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Settings
prd = 10
ppsrc = 'High/Low'  # 'High/Low' or 'Close/Open'
ChannelW = 5 / 100  # Convert percentage to decimal
minstrength = 1
maxnumsr = 6 - 1
loopback = 290

# Functions
def pivothigh(data, left_bars, right_bars):
    high_idx = data.rolling(window=left_bars + right_bars + 1).apply(lambda x: x[left_bars] == max(x), raw=True).astype(bool)
    return np.where(high_idx, data, np.nan)

def pivotlow(data, left_bars, right_bars):
    low_idx = data.rolling(window=left_bars + right_bars + 1).apply(lambda x: x[left_bars] == min(x), raw=True).astype(bool)
    return np.where(low_idx, data, np.nan)

# Calculate pivot points
df['src1'] = df['high'] if ppsrc == 'High/Low' else df[['close', 'open']].max(axis=1)
df['src2'] = df['low'] if ppsrc == 'High/Low' else df[['close', 'open']].min(axis=1)
df['ph'] = pivothigh(df['src1'].shift(prd), prd, prd)  # Shift for lookback
df['pl'] = pivotlow(df['src2'].shift(prd), prd, prd)

# Calculate channel width
prdhighest = df['high'].rolling(window=300).max()
prdlowest = df['low'].rolling(window=300).min()
df['cwidth'] = (prdhighest - prdlowest) * ChannelW

# Initialize Support/Resistance columns
for i in range(maxnumsr):
    df[f'SR_High_{i+1}'] = np.nan
    df[f'SR_Low_{i+1}'] = np.nan

# Loop through data
for i in range(loopback, len(df)):
    pivotvals = []
    pivotlocs = []
    for j in range(i - loopback, i + 1):
        if not pd.isna(df['ph'][j]) or not pd.isna(df['pl'][j]):
            pivotvals.insert(0, df['ph'][j] if not pd.isna(df['ph'][j]) else df['pl'][j])
            pivotlocs.insert(0, j)

    # Find/create SR channels
    supres = []
    stren = [0] * 10
    for k in range(len(pivotvals)):
        lo = pivotvals[k]
        hi = lo
        numpp = 0
        for l in range(len(pivotvals)):
            cpp = pivotvals[l]
            wdth = hi - cpp if cpp <= hi else cpp - lo
            if wdth <= df['cwidth'][i]:
                if cpp <= hi:
                    lo = min(lo, cpp)
                else:
                    hi = max(hi, cpp)
                numpp += 20
        supres.extend([numpp, hi, lo])

    # Calculate strength and update SR levels
    if len(supres) > 0:
        for k in range(len(pivotvals)):
            h = supres[k * 3 + 1]
            l = supres[k * 3 + 2]
            s = 0
            for m in range(i - loopback, i):
                if (df['high'][m] <= h and df['high'][m] >= l) or (df['low'][m] <= h and df['low'][m] >= l):
                    s += 1
            supres[k * 3] += s

        src = 0
        for k in range(len(pivotvals)):
            stv = -1
            stl = -1
            for l in range(len(pivotvals)):
                if supres[l * 3] > stv and supres[l * 3] >= minstrength * 20:
                    stv = supres[l * 3]
                    stl = l
            if stl >= 0:
                hh = supres[stl * 3 + 1]
                ll = supres[stl * 3 + 2]
                df.loc[i, f'SR_High_{src+1}'] = hh
                df.loc[i, f'SR_Low_{src+1}'] = ll
                stren[src] = supres[stl * 3]
                for l in range(len(pivotvals)):
                    if (supres[l * 3 + 1] <= hh and supres[l * 3 + 1] >= ll) or (
                            supres[l * 3 + 2] <= hh and supres[l * 3 + 2] >= ll):
                        supres[l * 3] = -1
                src += 1
                if src >= 10:
                    break

        # Sort SR levels by strength
        for k in range(8):
            for l in range(k + 1, 9):
                if stren[l] > stren[k]:
                    stren[k], stren[l] = stren[l], stren[k]
                    df.loc[i, f'SR_High_{k+1}'], df.loc[i, f'SR_High_{l+1}'] = df.loc[i, f'SR_High_{l+1}'], df.loc[i, f'SR_High_{k+1}']
                    df.loc[i, f'SR_Low_{k+1}'], df.loc[i, f'SR_Low_{l+1}'] = df.loc[i, f'SR_Low_{l+1}'], df.loc[i, f'SR_Low_{k+1}']

# Save the DataFrame to a CSV file
df.to_csv('data.csv', index=False)
