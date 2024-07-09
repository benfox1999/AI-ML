import pandas as pd
import numpy as np
import talib

# Load CSV data
df = pd.read_csv('data.csv')

# Convert timestamps to datetime objects if needed
# df['open_time'] = pd.to_datetime(df['open_time'])
# df['close_time'] = pd.to_datetime(df['close_time'])

# Feature Calculations
def calculate_features(df):
    df['RSI_14'] = talib.RSI(df['close'], timeperiod=14)
    df['WT_10_11'] = talib.WILLR(df['high'], df['low'], df['close'], timeperiod=10) - talib.WILLR(df['high'], df['low'], df['close'], timeperiod=11)
    df['CCI_20'] = talib.CCI(df['high'], df['low'], df['close'], timeperiod=20)
    df['ADX_20'] = talib.ADX(df['high'], df['low'], df['close'], timeperiod=20)
    df['RSI_9'] = talib.RSI(df['close'], timeperiod=9)
    return df

df = calculate_features(df)

# Lorentzian Distance
def lorentzian_distance(point1, point2):
    distance = np.sum(np.log(1 + np.abs(point1 - point2)))
    return distance

# Approximate Nearest Neighbors
def approximate_knn(df, neighbors_count):
    predictions = []
    for i in range(len(df)):
        if i < 2000 or i % 4 != 0:  # Skip initial bars and apply modulo logic
            predictions.append(0)  # Neutral prediction for skipped bars
            continue

        # Prepare feature vectors for current bar and historical data
        current_features = df.iloc[i][['RSI_14', 'WT_10_11', 'CCI_20', 'ADX_20', 'RSI_9']].values
        historical_features = df.iloc[:i][['RSI_14', 'WT_10_11', 'CCI_20', 'ADX_20', 'RSI_9']].values

        # Calculate Lorentzian distances
        distances = np.array([lorentzian_distance(current_features, historical_features[j]) for j in range(i)])

        # Find indices of nearest neighbors
        sorted_indices = np.argsort(distances)
        neighbor_indices = sorted_indices[:neighbors_count]

        # Determine prediction based on majority class of neighbors
        neighbor_labels = np.where(df['close'].iloc[neighbor_indices].shift(4).values < df['close'].iloc[neighbor_indices].values, 1, -1)  # Using shifted close for labels
        prediction = np.sum(neighbor_labels)
        predictions.append(prediction)

    return predictions

# Apply KNN and determine signals
df['prediction'] = approximate_knn(df, neighbors_count=8)  # Example: using 8 neighbors
df['signal'] = np.where((df['prediction'] > 0) & (df['close'] > df['close'].rolling(200).mean()), 1,
                        np.where((df['prediction'] < 0) & (df['close'] < df['close'].rolling(200).mean()), -1, 0))  # Example filter: EMA crossover

# Generate buy/sell signals
df['Machine Learning: Lorentzian Classification-buy'] = np.where(df['signal'] == 1, 1, 0)  # Buy signal
df['Machine Learning: Lorentzian Classification-sell'] = np.where(df['signal'] == -1, 1, 0)  # Sell signal

# Save the DataFrame back to CSV
df.to_csv('data.csv', index=False)
