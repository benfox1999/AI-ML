import pandas as pd
import numpy as np
import talib

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

# Define the Vortex Indicator function
def vortex_indicator(df, period_):
    df['High_Shift'] = df['high'].shift(1)
    df['Low_Shift'] = df['low'].shift(1)
    df['VMP'] = abs(df['high'] - df['Low_Shift'])
    df['VMM'] = abs(df['low'] - df['High_Shift'])
    df['ATR'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=1)
    df['VIP'] = df['VMP'].rolling(window=period_).sum() / df['ATR'].rolling(window=period_).sum()
    df['VIM'] = df['VMM'].rolling(window=period_).sum() / df['ATR'].rolling(window=period_).sum()
    return df

# Set the period for the Vortex Indicator
period_ = 14 

# Calculate the Vortex Indicator
df = vortex_indicator(df.copy(), period_)

# Add the calculated columns to the DataFrame
df['VI +'] = df['VIP']
df['VI -'] = df['VIM']

# Select specific columns for output
df = df[['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 
         'quote_volume', 'count', 'taker_buy_volume', 'taker_buy_quote_volume', 
         'ignore', 'VI +', 'VI -']]

# Save the updated DataFrame to the CSV file
df.to_csv('data.csv', index=False)
