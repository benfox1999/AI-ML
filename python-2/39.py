import pandas as pd
import numpy as np
import talib

# Load the CSV data
data = pd.read_csv("data.csv")

# Calculate cumulative volume
data['cumVol'] = data['volume'].cumsum()

# Check for zero volume
if data['cumVol'].iloc[-1] == 0:
    raise ValueError("No volume is provided by the data vendor.")

# Calculate Elder Force Index (EFI)
data['efi'] = (data['close'].diff() * data['volume']).ewm(span=13, adjust=False).mean()

# Rename the 'efi' column to 'Elder Force Index'
data.rename(columns={'efi': 'Elder Force Index'}, inplace=True)

# Save the updated data to the CSV file
data.to_csv("data.csv", index=False)
