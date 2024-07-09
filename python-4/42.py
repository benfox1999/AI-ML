import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Input parameters (mimicking Pine Script inputs)
src = df['close']
length = 2
percent = 1.4
mav_type = 'VAR'  # Options: 'SMA', 'EMA', 'WMA', 'TMA', 'VAR', 'WWMA', 'ZLEMA', 'TSF'

# --- Helper Functions (equivalent to Pine Script functions) ---
def Var_Func(src, length):
    valpha = 2 / (length + 1)
    src = pd.Series(src)  # Ensure it's a Series
    vud1 = pd.Series(np.where(src > src.shift(1), src - src.shift(1), 0))
    vdd1 = pd.Series(np.where(src < src.shift(1), src.shift(1) - src, 0))
    vUD = vud1.rolling(9).sum()
    vDD = vdd1.rolling(9).sum()
    vCMO = (vUD - vDD) / (vUD + vDD)
    vCMO = vCMO.fillna(0)
    VAR = np.zeros_like(src)
    VAR[0] = vCMO[0] * src[0]
    for i in range(1, len(src)):
        VAR[i] = valpha * abs(vCMO[i]) * src[i] + (1 - valpha * abs(vCMO[i])) * VAR[i - 1]
    return pd.Series(VAR)  # Convert back to Series explicitly

def Wwma_Func(src, length):
    wwalpha = 1 / length
    WWMA = np.zeros_like(src)
    WWMA[0] = src[0]
    for i in range(1, len(src)):
        WWMA[i] = wwalpha * src[i] + (1 - wwalpha) * WWMA[i - 1]
    return WWMA

def Zlema_Func(src, length):
    zxLag = length // 2 if length % 2 == 0 else (length - 1) // 2
    zxEMAData = src + (src - src.shift(zxLag))
    ZLEMA = talib.EMA(zxEMAData, length)
    return ZLEMA

def Tsf_Func(src, length):
    # Note: Linear regression in talib might not perfectly match Pine Script's
    lrc = talib.LINEARREG(src, length)
    lrc1 = talib.LINEARREG(src.shift(1), length)
    lrs = lrc - lrc1
    TSF = talib.LINEARREG(src, length) + lrs
    return TSF

def getMA(src, length, ma_type):
    src = pd.Series(src)
    if ma_type == 'SMA': return pd.Series(talib.SMA(src, length))  
    if ma_type == 'EMA': return pd.Series(talib.EMA(src, length))  
    if ma_type == 'WMA': return pd.Series(talib.WMA(src, length)) 
    if ma_type == 'TMA': 
        return pd.Series(talib.SMA(talib.SMA(src, (length + 1) // 2), length // 2 + 1))
    if ma_type == 'VAR': return Var_Func(src, length)  
    if ma_type == 'WWMA': return Wwma_Func(src, length) 
    if ma_type == 'ZLEMA': return Zlema_Func(src, length)  
    if ma_type == 'TSF': return Tsf_Func(src, length) 
    return None
# --- Main Calculation Logic ---
MAvg = pd.Series(getMA(src, length, mav_type))
fark = MAvg * percent * 0.01

# Ensure that rolling operations are done on Series
longStop = pd.Series(MAvg - fark).rolling(2).max()
shortStop = pd.Series(MAvg + fark).rolling(2).min() 

# dir calculation
dir_list = []
for i in range(len(MAvg)):
    if i == 0:
        dir_list.append(1)
    else:
        prev_dir = dir_list[-1]
        if prev_dir == -1 and MAvg.iloc[i] > shortStop.iloc[i - 1]:
            dir_list.append(1)
        elif prev_dir == 1 and MAvg.iloc[i] < longStop.iloc[i - 1]:
            dir_list.append(-1)
        else:
            dir_list.append(prev_dir)
dir = pd.Series(dir_list)

# Ensure MT and OTT are also Series before calculations
MT = pd.Series(np.where(dir == 1, longStop, shortStop)) 
OTT = pd.Series(np.where(MAvg > MT, MT * (200 + percent) / 200, MT * (200 - percent) / 200))

# --- Signal Generation ---
def crossover(series1, series2):
    """Detects crossovers of two series."""
    cond1 = (series1 > series2) & (series1.shift(1) <= series2.shift(1))  # series1 crosses above series2
    cond2 = (series1 < series2) & (series1.shift(1) >= series2.shift(1))  # series1 crosses below series2
    return pd.Series(np.where(cond1, 1, np.where(cond2, -1, 0)))  # 1 for crossover up, -1 for crossover down, 0 otherwise

# --- Signal Generation (Using custom crossover) ---
df['Optimized Trend Tracker-buy'] = np.where(crossover(MAvg, OTT.shift(2)) == 1, 1, 0)
df['Optimized Trend Tracker-sell'] = np.where(crossover(MAvg, OTT.shift(2)) == -1, 1, 0)

# --- Save to CSV ---
df.to_csv('data.csv', index=False)
