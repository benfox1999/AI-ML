import pandas as pd
import numpy as np
import talib

# Load CSV data
data = pd.read_csv("data.csv")

# Define inputs
perc = 1.0  # Percentage Step
nbr = 5  # Number of Lines

# Initialize variables
data['green'] = data['close'] > data['open']
data['red'] = data['close'] < data['open']
total = np.zeros((7, 4))
vals = np.zeros((5, 4))
lines = [None] * 10
labels = [None] * 10

# Score Calculation function
def Score(x, i, data, total, vals):
    ghh, gll = total[i, 0], total[i, 1]
    rhh, rll = total[i, 2], total[i, 3]
    gtotal, rtotal = total[5, 0], total[5, 1]
    
    data['hh'] = data['high'] >= data['high'].shift(1) + x
    data['ll'] = data['low'] <= data['low'].shift(1) - x
    
    for j in range(1, len(data)):
        if data['green'][j] and data['hh'][j]:
            total[i, 0] = ghh + 1
            vals[i, 0] = round(((ghh + 1) / gtotal) * 100, 2)
        if data['green'][j] and data['ll'][j]:
            total[i, 1] = gll + 1
            vals[i, 1] = round(((gll + 1) / gtotal) * 100, 2)
        if data['red'][j] and data['hh'][j]:
            total[i, 2] = rhh + 1
            vals[i, 2] = round(((rhh + 1) / rtotal) * 100, 2)
        if data['red'][j] and data['ll'][j]:
            total[i, 3] = rll + 1
            vals[i, 3] = round(((rll + 1) / rtotal) * 100, 2)
    
    return total, vals

# Backtest function
def Backtest(v, total):
    p1, p2 = total[6, 0], total[6, 1]
    for j in range(1, len(data)):
        if v[j] == data['high'][j - 1]:
            if data['high'][j] >= v[j]:
                total[6, 0] = p1 + 1
            else:
                total[6, 1] = p2 + 1
        else:
            if data['low'][j] <= v[j]:
                total[6, 0] = p1 + 1
            else:
                total[6, 1] = p2 + 1
    return total

# Calculate green and red candle counts
for i in range(len(data)):
    if data['green'][i]:
        total[5, 0] += 1
    if data['red'][i]:
        total[5, 1] += 1

# Calculate scores
data['step'] = data['close'] * (perc / 100)
total, vals = Score(0, 0, data.copy(), total, vals)
total, vals = Score(data['step'], 1, data.copy(), total, vals)
total, vals = Score(data['step'] * 2, 2, data.copy(), total, vals)
total, vals = Score(data['step'] * 3, 3, data.copy(), total, vals)
total, vals = Score(data['step'] * 4, 4, data.copy(), total, vals)

# Backtest
a1, b1 = vals[0, 0], vals[0, 1]
a2, b2 = vals[0, 2], vals[0, 3]
v = np.where(data['green'], np.where((a1 > b1), data['high'].shift(1), data['low'].shift(1)),
             np.where((a2 > b2), data['high'].shift(1), data['low'].shift(1)))
total = Backtest(v, total)

# Since we're not plotting, we only need the final calculated values for appending
data['Breakout Probability (Expo)'] = np.where(data['green'], np.where((a1 > b1), a1, b1),
             np.where((a2 > b2), a2, b2))

# Save updated data to CSV
data.to_csv("data.csv", index=False)
