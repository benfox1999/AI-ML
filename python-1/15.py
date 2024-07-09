import pandas as pd
import numpy as np

# Load data from CSV
df = pd.read_csv('data.csv')

# Initialize variables as pd.Series
df['uptrend'] = pd.Series(np.nan, index=df.index)
df['EP'] = pd.Series(np.nan, index=df.index)
df['SAR'] = pd.Series(np.nan, index=df.index)
df['nextBarSAR'] = pd.Series(np.nan, index=df.index)

start = 0.02
increment = 0.02
maximum = 0.2
AF = start

# Iterate through the DataFrame
for i in range(1, len(df)):
    # Initial calculations on the second bar
    if i == 1:
        if df['close'][i] > df['close'][i - 1]:
            df.loc[i, 'uptrend'] = True
            df.loc[i, 'EP'] = df['high'][i]
            prevSAR = df['low'][i - 1]
            prevEP = df['high'][i]
        else:
            df.loc[i, 'uptrend'] = False
            df.loc[i, 'EP'] = df['low'][i]
            prevSAR = df['high'][i - 1]
            prevEP = df['low'][i]

        df.loc[i, 'SAR'] = prevSAR + start * (prevEP - prevSAR)

    else:
        # Determine trend direction using .loc for assignments
        if df['uptrend'][i - 1]:
            if df['SAR'][i - 1] > df['low'][i]:
                df.loc[i, 'uptrend'] = False
                df.loc[i, 'SAR'] = max(df['EP'][i - 1], df['high'][i])
                df.loc[i, 'EP'] = df['low'][i]
                AF = start
            else:
                df.loc[i, 'uptrend'] = True
                df.loc[i, 'SAR'] = min(df['SAR'][i - 1], df['low'][i - 1])
                if i > 2:
                    df.loc[i, 'SAR'] = min(df['SAR'][i], df['low'][i - 2])
        else:
            if df['SAR'][i - 1] < df['high'][i]:
                df.loc[i, 'uptrend'] = True
                df.loc[i, 'SAR'] = min(df['EP'][i - 1], df['low'][i])
                df.loc[i, 'EP'] = df['high'][i]
                AF = start
            else:
                df.loc[i, 'uptrend'] = False
                df.loc[i, 'SAR'] = max(df['SAR'][i - 1], df['high'][i - 1])
                if i > 2:
                    df.loc[i, 'SAR'] = max(df['SAR'][i], df['high'][i - 2])

        # Update Extreme Point (EP) and Acceleration Factor (AF)
        if df['uptrend'][i]:
            if df['high'][i] > df['EP'][i]:
                df.loc[i, 'EP'] = df['high'][i]
                AF = min(AF + increment, maximum)
        else:
            if df['low'][i] < df['EP'][i]:
                df.loc[i, 'EP'] = df['low'][i]
                AF = min(AF + increment, maximum)

    # Calculate nextBarSAR
    df.loc[i, 'nextBarSAR'] = df['SAR'][i] + AF * (df['EP'][i] - df['SAR'][i])

# Generate trading signals
df['Parabolic SAR Strategy'] = np.where(df['uptrend'], 'sell', 'buy')

# Save the DataFrame back to CSV
df.to_csv('data.csv', index=False)
