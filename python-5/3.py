import pandas as pd
import numpy as np
from ta.trend import EMAIndicator
from ta.momentum import WilliamsRIndicator  # Using Williams %R to approximate fractals

# Load your data from CSV
df = pd.read_csv('data.csv')

# Input Parameters (Customize these)
fast_length = 20
medium_length = 50
slow_length = 100
fractal_period = 2
risk_reward_ratio = 1.5
max_loss_percentage = 1

# Calculate EMAs
ema_fast = EMAIndicator(close=df['close'], window=fast_length)
ema_medium = EMAIndicator(close=df['close'], window=medium_length)
ema_slow = EMAIndicator(close=df['close'], window=slow_length)

df['EMA_Fast'] = ema_fast.ema_indicator()
df['EMA_Medium'] = ema_medium.ema_indicator()
df['EMA_Slow'] = ema_slow.ema_indicator()

# Approximate Williams Fractals with Williams %R
williams_r = WilliamsRIndicator(high=df['high'], low=df['low'], close=df['close'], lbp=fractal_period)
df['Williams_R'] = williams_r.williams_r()

# Long/Short Entry Signals
df['Williams_R-longEntry'] = (
    (df['Williams_R'].shift(1) < -80) &  # Approximate "Fractal Up"
    (df['close'].shift(1) < df['EMA_Fast'].shift(1)) &
    (df['close'] > df['EMA_Fast']) &
    (df['EMA_Fast'] > df['EMA_Medium']) &
    (df['EMA_Medium'] > df['EMA_Slow'])
)

df['Williams_R-shortEntry'] = (
    (df['Williams_R'].shift(1) > -20) &  # Approximate "Fractal Down"
    (df['close'].shift(1) > df['EMA_Fast'].shift(1)) &
    (df['close'] < df['EMA_Fast']) &
    (df['EMA_Fast'] < df['EMA_Medium']) &
    (df['EMA_Medium'] < df['EMA_Slow'])
)

# Save updated DataFrame back to CSV
df.to_csv('data.csv', index=False)
