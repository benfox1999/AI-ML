import pandas as pd
import numpy as np

# Load the CSV data
df = pd.read_csv('data.csv')

# Convert timestamp columns to datetime objects
df['open_time'] = pd.to_datetime(df['open_time'])
df['close_time'] = pd.to_datetime(df['close_time'])

# Initialize variables
chain_length = 150
hide_zeros = False
minus_color = '#FC8083'  # Not used in calculations
plus_color = '#ADAEF4'  # Not used in calculations

def calculate_order_chain(df):
    """
    Calculates the order chain data and appends it to the DataFrame.

    Args:
      df: Pandas DataFrame containing stock data.

    Returns:
      Pandas DataFrame with the calculated 'Order Chain [Kioseff Trading]' column.
    """

    df['Order Chain [Kioseff Trading]'] = np.nan
    market_orders = []
    time_arr = []
    key_values = {'Top': 0, 'Bot': 20e25, 'Abs': 0, 'Max': 0}

    for i in range(1, len(df)):
        vol = df['volume'].iloc[i]
        vol1 = df['volume'].iloc[i - 1]
        c = df['close'].iloc[i]
        c1 = df['close'].iloc[i - 1]

        if vol > vol1 and vol1 != 0 and c != c1:
            direction = np.sign(c - c1)
            market_orders.append({
                'price': c,
                'volFlow': (vol - vol1) * direction,
                'location': 1,
            })

            key_values['Abs'] = max(key_values['Abs'], abs(vol - vol1))
            key_values['Max'] = max(key_values['Max'], c)

            if len(market_orders) > chain_length:
                market_orders.pop(0)

            if len(market_orders) > 1:
                time_arr.append(df['open_time'].iloc[i])
                if len(time_arr) > chain_length:
                    time_arr.pop(0)

                first_data = market_orders[-1]
                range_val = abs(key_values['Top'] - key_values['Bot'])
                normed_size = (0.05 + 0.1 * abs(first_data['volFlow']) / key_values['Abs']) * range_val * np.sign(
                    first_data['volFlow']
                )

                key_values['Top'] = max(
                    key_values['Top'], first_data['price'], first_data['price'] + normed_size
                )
                key_values['Bot'] = min(
                    key_values['Bot'], first_data['price'], first_data['price'] + normed_size
                )

    return df


# Calculate the order chain data and update the DataFrame
df = calculate_order_chain(df.copy())

# Save the updated DataFrame to a CSV file
df.to_csv('data.csv', index=False)
