import pandas as pd
import numpy as np
import talib

# Load data from CSV
df = pd.read_csv('data.csv', dtype={'14': float, '15': float, '354': float}, low_memory=False)

# Connors RSI Calculation
def ConnorsRSI(df, lenrsi=3, lenupdown=2, lenroc=100):
    close = df['close']

    # UpDown Calculation (vectorized and corrected)
    df['updown'] = 0
    df.loc[1:, 'updown'] = np.where(
        close[1:].reset_index(drop=True) == close[:-1].reset_index(drop=True),  # Align indices before comparison
        0,
        np.sign(close[1:].values - close[:-1].values) * (np.abs(df['updown'].shift(1)[1:]) + 1) 
    )

    # RSI, UpDown RSI, and Percent Rank Calculations
    df['rsi'] = talib.RSI(close, timeperiod=lenrsi)
    df['updownrsi'] = talib.RSI(df['updown'], timeperiod=lenupdown)
    df['percentrank'] = df['close'].pct_change(1).rank(pct=True) * 100

    # Connors RSI
    df['Connors RSI'] = (df['rsi'] + df['updownrsi'] + df['percentrank']) / 3

    return df

# Calculate Connors RSI
df = ConnorsRSI(df)

# Save the updated DataFrame to CSV
df.to_csv('data.csv', index=False)
