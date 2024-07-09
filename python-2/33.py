import pandas as pd
import numpy as np


# Load CSV data with type conversion for specific columns
data = pd.read_csv('data.csv', dtype={'14': float, '15': float, '354': float}, low_memory=False) 

# Define function to fetch advancing and declining volume data
def get_volume_data(exchange):
    adv_ticker = {
        "DJ": "UPVOL.DJ",
        "US Total": "UPVOL.US",
        "ARCX": "UPVOL.AX",
        "AMEX": "UPVOL.AM",
        "NASDAQ": "UPVOL.NQ",
        "NYSE": "UPVOL.NY"
    }.get(exchange, "UPVOL.NY")  # Default to NYSE

    dec_ticker = {
        "DJ": "DNVOL.DJ",
        "US Total": "DNVOL.US",
        "ARCX": "DNVOL.AX",
        "AMEX": "DNVOL.AM",
        "NASDAQ": "DNVOL.NQ",
        "NYSE": "DNVOL.NY"
    }.get(exchange, "DNVOL.NY")

    # ** Assuming 'adv' and 'dec' data is available - replace with actual data retrieval if needed
    # Example placeholder - replace with your data source
    adv = pd.Series(np.random.rand(len(data)), index=data.index)  # Convert to Series with index
    dec = pd.Series(np.random.rand(len(data)), index=data.index)

    return adv, dec

# Input exchange (replace with user input if needed)
exchange = "NYSE"

# Get advancing and declining volume data
adv, dec = get_volume_data(exchange)

# Calculate Cumulative Volume Index (CVI) using pandas `cumsum()`
data['Cumulative Volume Index'] = (adv - dec).cumsum()

# Save the updated DataFrame to the CSV file
data.to_csv('data.csv', index=False)
