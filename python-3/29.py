import pandas as pd
import numpy as np
import talib

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

def get_slopes(source1, source2):
    """Calculate slopes of two series."""
    m1 = source1.diff()
    m2 = source2.diff()
    return m1, m2

def common_scaling_factor(source1, source2, m1, m2):
    """Calculate the common scaling factor."""
    return (source1 - source2) / (m1 - m2)

def cross_value(source1, source2):
    """Calculate intersection value if a cross occurs."""
    insct = np.nan
    m1, m2 = get_slopes(source1, source2)
    cross_occurred = ((source1 > source2) & (source1.shift(1) < source2.shift(1))) | ((source1 < source2) & (source1.shift(1) > source2.shift(1)))
    if cross_occurred.any():
        sf = common_scaling_factor(source1[cross_occurred], source2[cross_occurred], m1[cross_occurred], m2[cross_occurred])
        insct = source1[cross_occurred] - sf * m1[cross_occurred]
    return insct

def crossover_value(source1, source2):
    """Calculate intersection value if a crossover occurs."""
    insct = np.nan
    m1, m2 = get_slopes(source1, source2)
    crossover_occurred = (source1 > source2) & (source1.shift(1) <= source2.shift(1)) 
    if crossover_occurred.any():
        sf = common_scaling_factor(source1[crossover_occurred], source2[crossover_occurred], m1[crossover_occurred], m2[crossover_occurred])
        insct = source1[crossover_occurred] - sf * m1[crossover_occurred]
    return insct

def crossunder_value(source1, source2):
    """Calculate intersection value if a crossunder occurs."""
    insct = np.nan
    m1, m2 = get_slopes(source1, source2)
    crossunder_occurred = (source1 < source2) & (source1.shift(1) >= source2.shift(1))
    if crossunder_occurred.any():
        sf = common_scaling_factor(source1[crossunder_occurred], source2[crossunder_occurred], m1[crossunder_occurred], m2[crossunder_occurred])
        insct = source1[crossunder_occurred] - sf * m1[crossunder_occurred]
    return insct
    
# Example usage: Assuming 'close' is the price column
df['SMA_9'] = talib.SMA(df['close'], timeperiod=9)
df['SMA_20'] = talib.SMA(df['close'], timeperiod=20)

df['Intersection Value Functions'] = cross_value(df['SMA_9'], df['SMA_20'])
df['Intersection Value Functions-crossover'] = crossover_value(df['SMA_9'], df['SMA_20'])
df['Intersection Value Functions-crossunder'] = crossunder_value(df['SMA_9'], df['SMA_20'])

# Save the updated DataFrame back to CSV
df.to_csv('data.csv', index=False)
