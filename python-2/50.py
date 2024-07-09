import pandas as pd
import numpy as np
from scipy.stats import linregress

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv', dtype={'14': float, '15': float, '354': float}, low_memory=False)

# Convert 'open_time' to datetime objects if necessary
df['open_time'] = pd.to_datetime(df['open_time'])  # Correct column name here

# Define the Pine Script function equivalent for Linear Regression
def calcSlope(source, length):
    x = np.arange(length) + 1
    y = source[-length:].reset_index(drop=True)  # Reset index for alignment
    if len(y) < length:
        return np.nan, np.nan, np.nan  # Return NaN if not enough data
    slope, intercept, r_value, _, _ = linregress(x, y)
    average = np.mean(y)
    return slope, average, intercept

# Set input parameters
lengthInput = 100
sourceInput = df['close'].astype(float)  # Convert to float
useUpperDevInput = True
upperMultInput = 2.0
useLowerDevInput = True
lowerMultInput = 2.0
showPearsonInput = True  # Not used in this calculation
extendLeftInput = False  # Not used in this calculation
extendRightInput = True  # Not used in this calculation

# Calculate Linear Regression values
s, a, i = calcSlope(sourceInput, lengthInput)
df['startPrice'] = i + s * (lengthInput - 1)
df['endPrice'] = i

# Calculate deviations
stdDev = df['close'].rolling(window=lengthInput).std()
upDev = (
    df['high'].rolling(window=lengthInput).max()
    - df['close'].rolling(window=lengthInput).mean()
)
dnDev = (
    df['close'].rolling(window=lengthInput).mean()
    - df['low'].rolling(window=lengthInput).min()
)

# Correctly calculate and assign channel lines using .loc[]
df.loc[lengthInput - 1 :, 'upperStartPrice'] = (
    df['startPrice'][lengthInput - 1 :]
    + np.where(useUpperDevInput, upperMultInput * stdDev, upDev)[lengthInput - 1 :]
)
df.loc[lengthInput - 1 :, 'upperEndPrice'] = (
    df['endPrice'][lengthInput - 1 :]
    + np.where(useUpperDevInput, upperMultInput * stdDev, upDev)[lengthInput - 1 :]
)
df.loc[lengthInput - 1 :, 'lowerStartPrice'] = (
    df['startPrice'][lengthInput - 1 :]
    + np.where(useLowerDevInput, -lowerMultInput * stdDev, -dnDev)[lengthInput - 1 :]
)
df.loc[lengthInput - 1 :, 'lowerEndPrice'] = (
    df['endPrice'][lengthInput - 1 :]
    + np.where(useLowerDevInput, -lowerMultInput * stdDev, -dnDev)[lengthInput - 1 :]
)

# Calculate trend
df['trend'] = np.sign(df['startPrice'] - df['endPrice'])

# Save the results to a new CSV file
df.to_csv('data.csv', index=False)
