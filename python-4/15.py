import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Define EMA periods
ema_slow_period = 62
ema_fast_period = 38

# Calculate EMAs
df['ema_slow'] = talib.EMA(df['close'], timeperiod=ema_slow_period)
df['ema_fast'] = talib.EMA(df['close'], timeperiod=ema_fast_period)

# Aggressive Entry/Alert
df['CM_SlingShotSystem-buy'] = np.where((df['ema_fast'] > df['ema_slow']) & (df['close'] < df['ema_fast']), 1, 0)
df['CM_SlingShotSystem-sell'] = np.where((df['ema_fast'] < df['ema_slow']) & (df['close'] > df['ema_fast']), 1, 0)

# Conservative Entry
df['CM_SlingShotSystem-buy'] = np.where((df['ema_fast'] > df['ema_slow']) & (df['close'].shift(1) < df['ema_fast']) & (df['close'] > df['ema_fast']), 1, df['CM_SlingShotSystem-buy'])
df['CM_SlingShotSystem-sell'] = np.where((df['ema_fast'] < df['ema_slow']) & (df['close'].shift(1) > df['ema_fast']) & (df['close'] < df['ema_fast']), 1, df['CM_SlingShotSystem-sell'])

# Save the updated DataFrame to a CSV file
df.to_csv('data.csv', index=False)
