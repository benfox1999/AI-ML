import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')
step="Auto"
# Convert timestamps if needed
df['open_time'] = pd.to_datetime(df['open_time'])
df['close_time'] = pd.to_datetime(df['close_time'])

def trailing_management(df, prd=20, perc=0.005, bias="Auto"):
    """Implements the Trailing Management strategy."""
    
    # AutoMove Calculation
    df['hi'] = df['high'].rolling(prd * 10).max()
    df['lo'] = df['low'].rolling(prd * 10).min()
    df['ph'] = df['high']
    df['pl'] = df['low']
    df['phL'] = np.nan
    df['plL'] = np.nan
    
    for i in range(prd, len(df)):
        max_idx = talib.MAXINDEX(df['high'].values[i - prd : i], prd)[0]
        min_idx = talib.MININDEX(df['low'].values[i - prd : i], prd)[0]

        df.loc[i, 'ph'] = df['high'].iloc[i] if max_idx == 0 else df['ph'].iloc[i - 1]
        df.loc[i, 'pl'] = df['low'].iloc[i] if min_idx == 0 else df['pl'].iloc[i - 1]
        df.loc[i, 'phL'] = i if max_idx == 0 else df['phL'].iloc[i - 1]
        df.loc[i, 'plL'] = i if min_idx == 0 else df['plL'].iloc[i - 1]
        
    df['dir'] = np.where(df['phL'] > df['plL'], 1, -1)
    df['longtsl'] = np.nan
    df['shorttsl'] = np.nan

    peaks = []
    for i in range(1, len(df)):
        if df['dir'].iloc[i] != df['dir'].iloc[i - 1]:
            peaks.append(
                (df['ph'].iloc[i - 1] - df['pl'].iloc[i]) / df['ph'].iloc[i - 1]
                if df['dir'].iloc[i] > 0
                else (df['ph'].iloc[i] - df['pl'].iloc[i - 1]) / df['pl'].iloc[i - 1]
            )
    autocalc = np.median(peaks) if len(peaks) > 0 else 0
    if step == "Auto":
        df['Switch'] = np.where(df['low'] < df['longtsl'], df['low'] - (df['low'] * autocalc), df['high'] + (df['high'] * autocalc))
    elif step == "Percentage":
        df['Switch'] = np.where(df['low'] < df['longtsl'], df['low'] - (df['low'] * perc), df['high'] + (df['high'] * perc))
    elif step == "Pivot":
        df['Switch'] = np.where(df['low'] < df['longtsl'], df['pl'], df['ph'])
    


    df['longtsl'] = np.nan
    df['shorttsl'] = np.nan
    df['pos'] = 0
    longtsl = 0 # set initial value to 0 
    shorttsl = 0 # set initial value to 0
    pos = 0

    for i in range(len(df)):
        # Use fillna(0) to fill None values with 0
        if df['low'].iloc[i] <= longtsl or pd.isna(longtsl):
            longtsl = df['Switch'].iloc[i] if not pd.isna(df['Switch'].iloc[i]) else longtsl
            shorttsl = df['Switch'].iloc[i] if not pd.isna(df['Switch'].iloc[i]) else shorttsl
            pos = -1
        if df['high'].iloc[i] >= shorttsl or pd.isna(shorttsl):
            longtsl = df['Switch'].iloc[i] if not pd.isna(df['Switch'].iloc[i]) else longtsl
            shorttsl = df['Switch'].iloc[i] if not pd.isna(df['Switch'].iloc[i]) else shorttsl
            pos = 1
        
        if bias == "Bullish":
            pos = 1
        elif bias == "Bearish":
            pos = -1

        df.loc[i, 'longtsl'] = longtsl
        df.loc[i, 'shorttsl'] = shorttsl
        df.loc[i, 'pos'] = pos

    return df


df = trailing_management(df.copy(), prd=20, perc=0.005, bias="Auto")

df.to_csv('data.csv', index=False)
