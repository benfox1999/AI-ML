import pandas as pd
import numpy as np
import talib

# Load the CSV data
df = pd.read_csv('data.csv')

# Define a function to apply conditions for various candlestick patterns
def apply_candlestick_conditions(df):
    # Doji
    df['Doji'] = np.where(abs(df['open'] - df['close']) <= (df['high'] - df['low']) * 0.05, 1, 0)

    # Evening Star
    df['Evening Star'] = np.where(
        (df['close'].shift(2) > df['open'].shift(2)) &
        (df['open'].shift(1).where(df['open'].shift(1) < df['close'].shift(1), df['close'].shift(1)) > df['close'].shift(2)) &
        (df['open'] < df['open'].shift(1).where(df['open'].shift(1) < df['close'].shift(1), df['close'].shift(1))) &
        (df['close'] < df['open']), 1, 0
    )

    # Morning Star
    df['Morning Star'] = np.where(
        (df['close'].shift(2) < df['open'].shift(2)) &
        (df['open'].shift(1).where(df['open'].shift(1) > df['close'].shift(1), df['close'].shift(1)) < df['close'].shift(2)) &
        (df['open'] > df['open'].shift(1).where(df['open'].shift(1) > df['close'].shift(1), df['close'].shift(1))) &
        (df['close'] > df['open']), 1, 0
    )

    # Shooting Star
    df['Shooting Star'] = np.where(
        (df['open'].shift(1) < df['close'].shift(1)) &
        (df['open'] > df['close'].shift(1)) &
        (df['high'] - df['open'].where(df['open'] > df['close'], df['close']) >= abs(df['open'] - df['close']) * 3) &
        (df['close'].where(df['close'] < df['open'], df['open']) - df['low'] <= abs(df['open'] - df['close'])), 1, 0
    )

    # Hammer
    df['Hammer'] = np.where(
        ((df['high'] - df['low']) > 3 * (df['open'] - df['close'])) &
        (((df['close'] - df['low']) / (0.001 + df['high'] - df['low'])) > 0.6) &
        (((df['open'] - df['low']) / (0.001 + df['high'] - df['low'])) > 0.6), 1, 0
    )

    # Inverted Hammer
    df['Inverted Hammer'] = np.where(
        ((df['high'] - df['low']) > 3 * (df['open'] - df['close'])) &
        (((df['high'] - df['close']) / (0.001 + df['high'] - df['low'])) > 0.6) &
        (((df['high'] - df['open']) / (0.001 + df['high'] - df['low'])) > 0.6), 1, 0
    )

    # Bearish Harami
    df['Bearish Harami'] = np.where(
        (df['close'].shift(1) > df['open'].shift(1)) &
        (df['open'] > df['close']) &
        (df['open'] <= df['close'].shift(1)) &
        (df['open'].shift(1) <= df['close']) &
        (df['open'] - df['close'] < df['close'].shift(1) - df['open'].shift(1)), 1, 0
    )

    # Bullish Harami
    df['Bullish Harami'] = np.where(
        (df['open'].shift(1) > df['close'].shift(1)) &
        (df['close'] > df['open']) &
        (df['close'] <= df['open'].shift(1)) &
        (df['close'].shift(1) <= df['open']) &
        (df['close'] - df['open'] < df['open'].shift(1) - df['close'].shift(1)), 1, 0
    )

    # Bearish Engulfing
    df['Bearish Engulfing'] = np.where(
        (df['close'].shift(1) > df['open'].shift(1)) &
        (df['open'] > df['close']) &
        (df['open'] >= df['close'].shift(1)) &
        (df['open'].shift(1) >= df['close']) &
        (df['open'] - df['close'] > df['close'].shift(1) - df['open'].shift(1)), 1, 0
    )

    # Bullish Engulfing
    df['Bullish Engulfing'] = np.where(
        (df['open'].shift(1) > df['close'].shift(1)) &
        (df['close'] > df['open']) &
        (df['close'] >= df['open'].shift(1)) &
        (df['close'].shift(1) >= df['open']) &
        (df['close'] - df['open'] > df['open'].shift(1) - df['close'].shift(1)), 1, 0
    )

    # Piercing Line
    df['Piercing Line'] = np.where(
        (df['close'].shift(1) < df['open'].shift(1)) &
        (df['open'] < df['low'].shift(1)) &
        (df['close'] > df['close'].shift(1) + ((df['open'].shift(1) - df['close'].shift(1)) / 2)) &
        (df['close'] < df['open'].shift(1)), 1, 0
    )

    # Bullish Belt Hold
    df['Bullish Belt Hold'] = np.where(
        (df['low'] == df['open']) &
        (df['open'] < pd.Series.rolling(df['low'], window=10).min().shift(1)) &
        (df['open'] < df['close']) &
        (df['close'] > ((df['high'].shift(1) - df['low'].shift(1)) / 2) + df['low'].shift(1)), 1, 0
    )

    # Bullish Kicker
    df['Bullish Kicker'] = np.where(
        (df['open'].shift(1) > df['close'].shift(1)) &
        (df['open'] >= df['open'].shift(1)) &
        (df['close'] > df['open']), 1, 0
    )

    # Bearish Kicker
    df['Bearish Kicker'] = np.where(
        (df['open'].shift(1) < df['close'].shift(1)) &
        (df['open'] <= df['open'].shift(1)) &
        (df['close'] <= df['open']), 1, 0
    )

    # Hanging Man
    df['Hanging Man'] = np.where(
        ((df['high'] - df['low']) > 4 * (df['open'] - df['close'])) &
        (((df['close'] - df['low']) / (0.001 + df['high'] - df['low'])) >= 0.75) &
        (((df['open'] - df['low']) / (0.001 + df['high'] - df['low'])) >= 0.75) &
        (df['high'].shift(1) < df['open']) &
        (df['high'].shift(2) < df['open']), 1, 0
    )

    # Dark Cloud Cover
    df['Dark Cloud Cover'] = np.where(
        (df['close'].shift(1) > df['open'].shift(1)) &
        (((df['close'].shift(1) + df['open'].shift(1)) / 2) > df['close']) &
        (df['open'] > df['close']) &
        (df['open'] > df['close'].shift(1)) &
        (df['close'] > df['open'].shift(1)) &
        ((df['open'] - df['close']) / (0.001 + (df['high'] - df['low'])) > 0.6), 1, 0
    )
    
    return df

# Apply the candlestick pattern identification function to the dataframe
df = apply_candlestick_conditions(df)

# Save the updated DataFrame to a CSV file
df.to_csv('data.csv', index=False)
