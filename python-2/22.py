import pandas as pd
import numpy as np

df = pd.read_csv("data.csv")

def calculate_cmf(df, length=20):
    df['ad'] = np.where((df['close'] == df['high']) & (df['close'] == df['low']) | (df['high'] == df['low']), 0,
                    ((2 * df['close'] - df['low'] - df['high']) / (df['high'] - df['low'])) * df['volume'])
    df['mf'] = df['ad'].rolling(window=length).sum() / df['volume'].rolling(window=length).sum()
    return df

df = calculate_cmf(df)
df.to_csv("data.csv", index=False)
