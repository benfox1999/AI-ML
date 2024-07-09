import pandas as pd
import numpy as np
import talib

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

# Define the Pine Script functions in Python

def sma(src, length):
    return talib.SMA(src, length)

def atr(high, low, close, length):
    return talib.ATR(high, low, close, length)

def ema(src, length):
    return talib.EMA(src, length)

def wma(src, length):
    return talib.WMA(src, length)

def linreg(src, length, offset):
    return talib.LINEARREG(src, length) - offset * talib.LINEARREG_SLOPE(src, length)

def Var_Func(src, length):
    valpha = 2 / (length + 1)
    vud1 = np.where(src > src.shift(1), src - src.shift(1), 0)
    vdd1 = np.where(src < src.shift(1), src.shift(1) - src, 0)
    vUD = vud1.rolling(9).sum()
    vDD = vdd1.rolling(9).sum()
    vCMO = (vUD - vDD) / (vUD + vDD)
    vCMO[np.isnan(vCMO)] = 0  # Replace NaN values with 0
    VAR = np.zeros_like(src)
    VAR[1:] = (valpha * np.abs(vCMO[1:]) * src[1:]) + ((1 - valpha * np.abs(vCMO[1:])) * VAR[:-1])
    return VAR

def Wwma_Func(src, length):
    wwalpha = 1 / length
    WWMA = np.zeros_like(src)
    WWMA[1:] = (wwalpha * src[1:]) + ((1 - wwalpha) * WWMA[:-1])
    return WWMA

def Zlema_Func(src, length):
    zxLag = length // 2 if length % 2 == 0 else (length - 1) // 2
    zxEMAData = (src + (src - src.shift(zxLag)))
    return ema(zxEMAData, length)

def Tsf_Func(src, length):
    lrc = linreg(src, length, 0)
    lrc1 = linreg(src, length, 1)
    lrs = (lrc - lrc1)
    return linreg(src, length, 0) + lrs

def getMA(src, length, mav):
    if mav == "SMA":
        return sma(src, length)
    elif mav == "EMA":
        return ema(src, length)
    elif mav == "WMA":
        return wma(src, length)
    elif mav == "TMA":
        return sma(sma(src, int(np.ceil(length / 2))), int(np.floor(length / 2)) + 1)
    elif mav == "VAR":
        return Var_Func(src, length)
    elif mav == "WWMA":
        return Wwma_Func(src, length)
    elif mav == "ZLEMA":
        return Zlema_Func(src, length)
    elif mav == "TSF":
        return Tsf_Func(src, length)
    else:
        return None

def Pmax_Func(src, length, Multiplier, mav):
    MAvg = getMA(src, length, mav)
    longStop = MAvg - Multiplier * atr(df['high'], df['low'], df['close'], length)
    longStopPrev = longStop.shift(1).fillna(longStop)
    longStop = np.where(MAvg > longStopPrev, np.maximum(longStop, longStopPrev), longStop)
    shortStop = MAvg + Multiplier * atr(df['high'], df['low'], df['close'], length)
    shortStopPrev = shortStop.shift(1).fillna(shortStop)
    shortStop = np.where(MAvg < shortStopPrev, np.minimum(shortStop, shortStopPrev), shortStop)
    dir = np.zeros_like(src)
    dir[1:] = np.where((dir[:-1] == -1) & (MAvg[1:] > shortStopPrev[1:]), 1,
                       np.where((dir[:-1] == 1) & (MAvg[1:] < longStopPrev[1:]), -1, dir[:-1]))
    dir = dir.astype(int)
    PMax = np.where(dir == 1, longStop, shortStop)
    return PMax

# Set the input values
Periods = 10
Multiplier = 3.0
mav = "EMA"
length = 10

# Calculate PMax
df['PMax Explorer'] = Pmax_Func(df['close'], length, Multiplier, mav)

# Calculate buy and sell signals
df['PMax Explorer-buy'] = ((df['PMax Explorer'].shift(1) > df['close'].shift(1)) & (df['PMax Explorer'] < df['close'])).astype(int)
df['PMax Explorer-sell'] = ((df['PMax Explorer'].shift(1) < df['close'].shift(1)) & (df['PMax Explorer'] > df['close'])).astype(int)

# Save the DataFrame to a CSV file
df.to_csv('data.csv', index=False)
