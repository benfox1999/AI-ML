import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Convert timestamp columns to datetime objects
df['open_time'] = pd.to_datetime(df['open_time'])
df['close_time'] = pd.to_datetime(df['close_time'])

# --- INPUT PARAMETERS (Match Pine Script settings) ---
timzon = "GMT-5"  # Timezone (not used in current calculation)
tFrm = "1m"       # Lower Timeframe (adjust if needed)
nRow = 62         # Length (60 + 2)
iVol = "Volume"    # Size Type ("Volume" or "Price Volume")
cFlsh = True      # Enable Flash
vFlsh = 8         # Flash Volume Threshold

# Function to get lower timeframe data
def get_lower_timeframe_data(df, timeframe):
    """Fetches 1S data (currently the only supported timeframe)."""
    if timeframe != "1m":
        raise NotImplementedError("Only '1S' timeframe is currently supported.")
    return df.copy()


def calculate_volume_speed(df, nRow, iVol, timfram, cFlsh, vFlsh):
    """Calculates volume speed and flash indicators."""
    
    # Initialize variables and matrix
    mtx = np.full((nRow, 4), np.nan)
    chg, upVol, dnVol = 0, 0, 0
    spkTim, spkDic, spkVol = np.nan, np.nan, np.nan
    avgSp_list, flash_list = [], []

    for i in range(nRow - 1, len(df)):
        cCls = df.iloc[i]['close']
        cVol = df.iloc[i]['volume'] if iVol == "Volume" else df.iloc[i]['volume'] * df.iloc[i]['close']

        # Update matrix
        mtx = np.roll(mtx, -1, axis=0)
        mtx[-1, :] = [df.iloc[i]['open_time'].timestamp(), np.nan, cCls, cVol]

        if i > nRow:
            pCls = mtx[-2, 2]
            chg = 1 if (cCls - pCls) / pCls > 0 else -1
            mtx[-1, 1] = chg

        # Volume Speed Calculation (after nRow + 1)
        if i > nRow + 1:
            for j in range(mtx.shape[0] - 3):
                upVol += mtx[j, 3] if mtx[j, 1] > 0 else 0
                dnVol += mtx[j, 3] if mtx[j, 1] < 0 else 0

            span = (mtx[-1, 0] - mtx[-3, 0]) / pd.to_timedelta(timfram).total_seconds()
            smVol = upVol + dnVol
            avVol = smVol / (mtx.shape[0] - 2)
            speed = smVol / span if span != 0 else 0
            avgSp_list.append(speed)

            # Flash Logic
            lstVol = mtx[-1, 3]
            if cFlsh and lstVol >= avVol * vFlsh:
                spkTim = mtx[-1, 0] + 3  # Assuming timestamp in seconds
                spkDic = mtx[-1, 1]
                spkVol = lstVol

            flash_list.append(1 if cFlsh and spkTim > mtx[-1, 0] and spkVol >= avVol * vFlsh else 0)

            upVol = 0
            dnVol = 0
        else:
            avgSp_list.append(np.nan)
            flash_list.append(0)

    return avgSp_list, flash_list


# --- MAIN CALCULATION ---

df_1s = get_lower_timeframe_data(df.copy(), tFrm)  # Get 1S data
speed, flash = calculate_volume_speed(df_1s, nRow, iVol, tFrm, cFlsh, vFlsh)  # Calculate speed & flash

speed = [np.nan] * (nRow - 1) + speed  # Add NaN for initial rows
flash = [0] * (nRow - 1) + flash    # Add 0 for initial rows



df['Volume Speed [MUQWISHI]-speed'] = speed  # Add speed column
df['Volume Speed [MUQWISHI]-flash'] = flash  # Add flash column

# Save the updated DataFrame
df.to_csv('data.csv', index=False)
