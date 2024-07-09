import pandas as pd
import numpy as np
import talib

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

# Define the input parameters
pctP = 66  # Percentage Input For PBars
pblb = 6   # PBars Look Back Period
pctS = 5   # Percentage Input For Shaved Bars
spb = False  # Show Pin Bars?
ssb = False  # Show Shaved Bars?
sib = False  # Show Inside Bars?
sob = False  # Show Outside Bars?
sgb = False  # Check Box To Turn Bars Gray?

# Calculate the percentage values
pctCp = pctP * 0.01
pctCPO = 1 - pctCp
pctCs = pctS * 0.01
pctSPO = pctCs

# Calculate the range
df['range'] = df['high'] - df['low']

# Define the functions for the different bar types
def pBarUp(df, i):
  return spb and df['open'][i] > df['high'][i] - (df['range'][i] * pctCPO) and df['close'][i] > df['high'][i] - (df['range'][i] * pctCPO) and df['low'][i] <= df['low'][i-pblb+1:i].min() 

def pBarDn(df, i):
  return spb and df['open'][i] < df['high'][i] - (df['range'][i] * pctCp) and df['close'][i] < df['high'][i] - (df['range'][i] * pctCp) and df['high'][i] >= df['high'][i-pblb+1:i].max()

def sBarUp(df, i):
  return ssb and (df['close'][i] >= (df['high'][i] - (df['range'][i] * pctCs)))

def sBarDown(df, i):
  return ssb and df['close'][i] <= (df['low'][i] + (df['range'][i] * pctCs))

def insideBar(df, i):
  return sib and df['high'][i] <= df['high'][i-1] and df['low'][i] >= df['low'][i-1] 

def outsideBar(df, i):
  return sob and (df['high'][i] > df['high'][i-1] and df['low'][i] < df['low'][i-1])

# Create the columns for the different bar types
df['CM_Price-Action-Bars'] = np.nan

# Iterate over the DataFrame and apply the functions
for i in range(pblb, len(df)):
  df['CM_Price-Action-Bars'][i] = any([pBarUp(df,i), pBarDn(df, i), sBarUp(df, i), sBarDown(df, i), insideBar(df, i), outsideBar(df, i)])

df['CM_Price-Action-Bars'] = df['CM_Price-Action-Bars'].astype('Int64')
# Save the updated DataFrame to a new CSV file
df.to_csv('data.csv', index=False)
