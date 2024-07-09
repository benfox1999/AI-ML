import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

def calculate_mavw(close_prices, fmal, smal, tmal, Fmal, Ftmal, Smal):
    M1 = talib.WMA(close_prices, timeperiod=fmal)
    M2 = talib.WMA(M1, timeperiod=smal)
    M3 = talib.WMA(M2, timeperiod=tmal)
    M4 = talib.WMA(M3, timeperiod=Fmal)
    M5 = talib.WMA(M4, timeperiod=Ftmal)
    MAVW = talib.WMA(M5, timeperiod=Smal)
    return MAVW

# Calculate MAVW
df['MavilimW'] = calculate_mavw(df['close'], 3, 5, 8, 13, 21, 34)

# Buy/Sell Signals
df['MavilimW-buy'] = np.where(df['MavilimW'] > df['MavilimW'].shift(1), 1, 0)  
df['MavilimW-sell'] = np.where(df['MavilimW'] < df['MavilimW'].shift(1), 1, 0)

# Save the updated DataFrame to 'data.csv'
df.to_csv('data.csv', index=False)
