import pandas as pd
import numpy as np

# Load CSV data
df = pd.read_csv('data.csv')

# Convert timestamps if necessary (assuming they are in milliseconds)
# df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
# df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')

def liquidity_price_depth_chart(df):
    showBullMax = True 
    showBearMax = True

    df['Liquidity Price Depth Chart [LuxAlgo]'] = np.nan

    x1 = None
    max_price = None
    max_bull_vol = None
    min_price = None
    max_bear_vol = None

    bull_map = {}
    bear_map = {}

    for i in range(len(df)):
        # Initialization if at the beginning of visible range
        if i == 0:
            x1 = i
            max_price = df['high'][i]
            max_bull_vol = df['volume'][i] if df['close'][i] > df['open'][i] else 0
            min_price = df['low'][i]
            max_bear_vol = df['volume'][i] if df['close'][i] < df['open'][i] else 0

        # Populate price/volume map
        if df['close'][i] > df['open'][i]:
            bull_map[df['close'][i]] = df['volume'][i]
            max_bull_vol = max(df['volume'][i], max_bull_vol)
        elif df['close'][i] < df['open'][i]:
            bear_map[df['close'][i]] = df['volume'][i]
            max_bear_vol = max(df['volume'][i], max_bear_vol)

        # Update max/min prices
        max_price = max(df['high'][i], max_price)
        min_price = min(df['low'][i], min_price)

        # Calculate and append values at the end of the visible range
        if i == len(df) - 1: 
            # Sorting (not as efficient as Pine's built-in sorting)
            bull_sorted = sorted(bull_map, reverse=True)
            bear_sorted = sorted(bear_map, reverse=True)

            bull_sumv = sum(bull_map.values())
            bear_sumv = sum(bear_map.values())

            bull_idx = 0.0
            bear_idx = 0.0

            for price in bull_sorted:
                bull_idx += bull_map[price] / bull_sumv
                # Simplified logic for demonstration (no plotting in Python equivalent)
                if bull_map[price] == max_bull_vol and showBullMax:
                    pass  # Logic for line drawing would go here

            for price in bear_sorted:
                bear_idx += bear_map[price] / bear_sumv
                if bear_map[price] == max_bear_vol and showBearMax:
                    pass  # Logic for line drawing would go here

            # Simplified calculation for demonstration (no area/box drawing)
            df.loc[df.index[-1], 'Liquidity Price Depth Chart [LuxAlgo]'] = bull_sumv / (bull_sumv + bear_sumv)

    return df

df = liquidity_price_depth_chart(df)

df.to_csv('data.csv', index=False) 
