import pandas as pd
import numpy as np
import talib

# Load data from CSV
df = pd.read_csv('data.csv')

# Settings
mtV = True  # Volume * currency
barsBack = 20000  # Amount of bars
iStep = 'Round'  # Round or Step
mlt = 0  # Rounding multiplier
step = 1  # Step size
offset = 200  # Offset
width = 205  # Max width Volume Profile

# --- Functions ---

def round_source(src):
    """Applies rounding to the source data based on settings."""
    if iStep == 'Step':
        return round(src / step) * step
    elif mlt > 0:
        return round(src / 10**mlt) * 10**mlt
    else:
        return round(src)

# --- Data Processing ---

df['src'] = round_source(df['close'])

# Calculate Volume Profile
originalMap = {}
for i in range(max(0, len(df) - barsBack), len(df)):  
    src = df['src'][i]
    volume = df['volume'][i] * df['src'][i] if mtV else df['volume'][i]
    originalMap[src] = originalMap.get(src, 0) + volume


# Find 3 highest volume levels
maxV = [(0, 0)] * 3
for key, value in originalMap.items():
    maxV.sort()
    if value > maxV[0][1]:
        maxV[0] = (key, value)

# Calculate width scaling factor
w = width / maxV[0][1]

# Create Volume Profile columns (replace with your desired logic)
df['Volume Profile with a few polylines'] = np.nan 

# Save updated data to CSV
df.to_csv('data.csv', index=False) 
