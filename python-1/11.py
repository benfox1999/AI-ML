import pandas as pd
import numpy as np

# Load CSV data
df = pd.read_csv('data.csv')

# Define momentum function
def momentum(seria, length):
    mom = seria - seria.shift(length)
    return mom

# Set input parameter
length = 12

# Calculate momentum indicators
df['mom0'] = momentum(df['close'], length)
df['mom1'] = momentum(df['mom0'], 1)

# Generate trading signals
df['Momentum Strategy-buy'] = np.where((df['mom0'] > 0) & (df['mom1'] > 0), 1, 0)
df['Momentum Strategy-sell'] = np.where((df['mom0'] < 0) & (df['mom1'] < 0), 1, 0)

# Save the updated DataFrame to a CSV file
df.to_csv('data.csv', index=False)

