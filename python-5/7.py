import pandas as pd
import numpy as np
from datetime import datetime

# Load the dataset
data = pd.read_csv('data.csv')

# Convert timestamps to datetime
data['open_time'] = pd.to_datetime(data['open_time'])
data['close_time'] = pd.to_datetime(data['close_time'])
# Set the start and stop dates
start_date = data['open_time'][0]
stop_date = data['open_time'][len(data)-1]

# Filter the data within the date range
data = data[(data['open_time'] >= start_date) & (data['close_time'] <= stop_date)]

# Calculate the RSI indicator
def rsi(series, window):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

short_window = 14
long_window = 28

data['knn_prediction-rsi_short'] = rsi(data['close'], short_window)
data['knn_prediction-rsi_long'] = rsi(data['close'], long_window)

# Calculate kNN prediction (simplified for demonstration)
def knn_prediction(data, k=252):
    predictions = []
    for i in range(len(data)):
        distances = np.sqrt((data['rsi_short'] - data['rsi_short'].iloc[i])**2 + (data['rsi_long'] - data['rsi_long'].iloc[i])**2)
        neighbors = data.iloc[distances.nsmallest(k).index]
        prediction = neighbors['close'].mean()
        predictions.append(prediction)
    return predictions

data['knn_prediction'] = knn_prediction(data)

# Save the updated data to a new CSV file
data.to_csv('data.csv', index=False)
