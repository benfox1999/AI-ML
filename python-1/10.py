import pandas as pd
import numpy as np

# Load CSV data
df = pd.read_csv("data.csv")

def momentum(seria, length):
    mom = seria - seria.shift(length)
    return mom

df['mom0'] = momentum(df['close'], 12)
df['mom1'] = momentum(df['mom0'], 1)

# Initialize 'MomLE' and 'MomSE' columns as pd.Series
df['MomLE'] = pd.Series(0, index=df.index)
df['MomSE'] = pd.Series(0, index=df.index)

# Generate trading signals using .loc for assignments
for i in range(len(df)):
    if df['mom0'][i] > 0 and df['mom1'][i] > 0:
        df.loc[i, 'MomLE'] = 1  # Buy signal
    if df['mom0'][i] < 0 and df['mom1'][i] < 0:
        df.loc[i, 'MomSE'] = 1  # Sell signal

# Save the updated DataFrame to 'data.csv'
df.to_csv("data.csv", index=False)
import pandas as pd
import numpy as np

# Load CSV data
df = pd.read_csv("data.csv")

def momentum(seria, length):
    mom = seria - seria.shift(length)
    return mom

df['mom0'] = momentum(df['close'], 12)
df['mom1'] = momentum(df['mom0'], 1)

# Initialize 'MomLE' and 'MomSE' columns as pd.Series
df['MomLE'] = pd.Series(0, index=df.index)
df['MomSE'] = pd.Series(0, index=df.index)

# Generate trading signals using .loc for assignments
for i in range(len(df)):
    if df['mom0'][i] > 0 and df['mom1'][i] > 0:
        df.loc[i, 'MomLE'] = 1  # Buy signal
    if df['mom0'][i] < 0 and df['mom1'][i] < 0:
        df.loc[i, 'MomSE'] = 1  # Sell signal

# Save the updated DataFrame to 'data.csv'
df.to_csv("data.csv", index=False)
