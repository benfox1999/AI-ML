import pandas as pd
import numpy as np
import talib

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

# --- Input Parameters (mimicking Pine Script inputs) ---
close_gaps_partially = False
box_limit = 15
minimal_deviation_percentage = 30.0
limit_box_length_bool = False
limit_box_length_int = 300

# --- Helper Functions ---
def calculate_minimal_deviation(df):
    df['hl_range'] = df['high'] - df['low']
    return df['hl_range'].rolling(14).mean() * (minimal_deviation_percentage / 100)

def register_new_gap(df, i, is_gap_down):
    if is_gap_down:
        df.loc[i, 'Gaps'] = df.loc[i - 1, 'low'] 
    else:
        df.loc[i, 'Gaps'] = df.loc[i - 1, 'high']

# --- Main Logic ---

# Calculate Minimal Deviation
df['minimal_deviation'] = calculate_minimal_deviation(df)
df['minimal_deviation'].fillna(method='bfill', inplace=True) # Fill initial NaN values

# Initialize 'Gaps' column 
df['Gaps'] = np.nan

# Loop through the DataFrame to detect gaps and closures
for i in range(1, len(df)):
    is_gap_down = df.loc[i, 'high'] < df.loc[i - 1, 'low'] and (df.loc[i - 1, 'low'] - df.loc[i, 'high']) >= df.loc[i, 'minimal_deviation']
    is_gap_up = df.loc[i, 'low'] > df.loc[i - 1, 'high'] and (df.loc[i, 'low'] - df.loc[i - 1, 'high']) >= df.loc[i, 'minimal_deviation']
    
    if is_gap_down or is_gap_up:
        register_new_gap(df, i, is_gap_down)

# ... (Logic for gap closure would require additional state management and is omitted for brevity) ... 

# Save the updated DataFrame to a new CSV file or overwrite the existing one
df.to_csv('data.csv', index=False) 
