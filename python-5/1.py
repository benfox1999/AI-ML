import pandas as pd
import numpy as np
from ta.trend import MACD, SMAIndicator

# Load your data from CSV (replace 'your_data.csv' with your actual file name)
df = pd.read_csv('data.csv')

# MACD Calculation
macd_indicator = MACD(close=df['close'], window_fast=12, window_slow=26, window_sign=9)
df['MACD'] = macd_indicator.macd()
df['MACD_Signal'] = macd_indicator.macd_signal()

# 200-day SMA Calculation
sma_indicator = SMAIndicator(close=df['close'], window=200)
df['SMA_200'] = sma_indicator.sma_indicator()

# Long/Short Entry Signals (Boolean columns)
df['MACD_Signal-yt-longEntry'] = ((df['MACD'] > df['MACD_Signal']) & 
                  (df['MACD'].shift(1) <= df['MACD_Signal'].shift(1)) & 
                  (df['MACD'] < 0) & 
                  (df['close'] > df['SMA_200']))

df['MACD_Signal-yt-shortEntry'] = ((df['MACD'] < df['MACD_Signal']) & 
                   (df['MACD'].shift(1) >= df['MACD_Signal'].shift(1)) & 
                   (df['MACD'] > 0) & 
                   (df['close'] < df['SMA_200']))

# Save updated DataFrame back to CSV
df.to_csv('data.csv', index=False)  
