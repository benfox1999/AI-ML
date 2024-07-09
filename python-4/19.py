import pandas as pd
import numpy as np
import talib

# Load data from CSV
df = pd.read_csv('data.csv')

# Define strategy function
def macd_sma_strategy(df, fast_length=12, slow_length=26, signal_length=9, veryslow_length=200):
    # Calculate indicators
    df['fast_ma'] = talib.SMA(df['close'], timeperiod=fast_length)
    df['slow_ma'] = talib.SMA(df['close'], timeperiod=slow_length)
    df['veryslow_ma'] = talib.SMA(df['close'], timeperiod=veryslow_length)
    df['macd'], df['macd_signal'], df['macd_hist'] = talib.MACD(df['close'], fastperiod=fast_length, slowperiod=slow_length, signalperiod=signal_length)

    # Identify buy and sell signals
    df['buy_signal'] = np.where(
        (df['macd_hist'].shift(1) < 0) & (df['macd_hist'] > 0) & (df['macd'] > 0) &
        (df['fast_ma'] > df['slow_ma']) & (df['close'].shift(slow_length) > df['veryslow_ma']), 1, 0)

    df['sell_signal'] = np.where(
        (df['macd_hist'].shift(1) > 0) & (df['macd_hist'] < 0) & (df['macd'] < 0) &
        (df['fast_ma'] < df['slow_ma']) & (df['close'].shift(slow_length) < df['veryslow_ma']), 1, 0)

    # Create strategy columns
    df['MACD + SMA 200 Strategy (by ChartArt)-buy'] = df['buy_signal']
    df['MACD + SMA 200 Strategy (by ChartArt)-sell'] = df['sell_signal']

    return df

# Apply strategy and update DataFrame
df = macd_sma_strategy(df)

# Save the updated DataFrame to the same CSV file
df.to_csv('data.csv', index=False)

