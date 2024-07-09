import pandas as pd
import numpy as np
import talib

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

def confidence(pearsonR):
    if pearsonR < 0.2:
        return "Extremely Weak"
    elif pearsonR < 0.3:
        return "Very Weak"
    elif pearsonR < 0.4:
        return "Weak"
    elif pearsonR < 0.5:
        return "Mostly Weak"
    elif pearsonR < 0.6:
        return "Somewhat Weak"
    elif pearsonR < 0.7:
        return "Moderately Weak"
    elif pearsonR < 0.8:
        return "Moderate"
    elif pearsonR < 0.9:
        return "Moderately Strong"
    elif pearsonR < 0.92:
        return "Mostly Strong"
    elif pearsonR < 0.94:
        return "Strong"
    elif pearsonR < 0.96:
        return "Very Strong"
    elif pearsonR < 0.98:
        return "Exceptionally Strong"
    else:
        return "Ultra Strong"

def calc_dev(source, length):
    """Calculate deviations for given length."""
    log_source = np.log(source)
    period_1 = length - 1
    
    # Initialize output arrays
    std_dev = np.full(len(source), np.nan)
    pearson_r = np.full(len(source), np.nan)
    slope = np.full(len(source), np.nan)
    intercept = np.full(len(source), np.nan)

    for i in range(length - 1, len(source)):
        sum_x = sum_xx = sum_yx = sum_y = 0.0
        for j in range(length):
            l_src = log_source[i - j]
            k = j + 1
            sum_x += k
            sum_xx += k * k
            sum_yx += k * l_src
            sum_y += l_src

        slope_val = (length * sum_yx - sum_x * sum_y) / (length * sum_xx - sum_x * sum_x) if (length * sum_xx - sum_x * sum_x) != 0 else np.nan
        average = sum_y / length
        intercept_val = average - (slope_val * sum_x / length) + slope_val

        sum_dev = sum_dxx = sum_dyy = sum_dyx = 0.0
        regres = intercept_val + slope_val * period_1 * 0.5
        sum_slp = intercept_val
        for j in range(period_1 + 1):
            l_src = log_source[i - j]
            dxt = l_src - average
            dyt = sum_slp - regres
            l_src -= sum_slp
            sum_slp += slope_val
            sum_dxx += dxt * dxt
            sum_dyy += dyt * dyt
            sum_dyx += dxt * dyt
            sum_dev += l_src * l_src

        un_std_dev = np.sqrt(sum_dev / period_1)
        divisor = sum_dxx * sum_dyy
        pearson_r_val = sum_dyx / np.sqrt(divisor) if divisor != 0 else np.nan
        
        std_dev[i] = un_std_dev
        pearson_r[i] = pearson_r_val
        slope[i] = slope_val
        intercept[i] = intercept_val

    return std_dev, pearson_r, slope, intercept

# Parameters (replace with user inputs if needed)
period_mode = False  # Use Long-Term Channel (True/False)
dev_multiplier = 2.0

# Define periods based on period mode
periods = np.array([300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200]) if period_mode else np.array([20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200])

# Calculate deviations and other values
results = []
for i in range(len(periods)):
    std_dev, pearson_r, slope, intercept = calc_dev(df['close'], int(periods[i]))
    results.append([std_dev, pearson_r, slope, intercept])

# Find the highest Pearson's R and corresponding values
highest_pearson_r = np.full(len(df), np.nan)
detected_period = np.full(len(df), np.nan)
detected_slope = np.full(len(df), np.nan)
detected_intrcpt = np.full(len(df), np.nan)
detected_std_dev = np.full(len(df), np.nan)

for i in range(len(df)):
    if i < max(periods):
        continue  # Skip calculations if not enough historical data
    max_pearson_r = -np.inf
    max_index = -1
    for j in range(len(periods)):
        if results[j][1][i] > max_pearson_r:
            max_pearson_r = results[j][1][i]
            max_index = j

    highest_pearson_r[i] = max_pearson_r
    detected_period[i] = periods[max_index]
    detected_slope[i] = results[max_index][2][i]
    detected_intrcpt[i] = results[max_index][3][i]
    detected_std_dev[i] = results[max_index][0][i]

# Calculate start and end prices for base, upper, and lower lines
start_price = np.exp(detected_intrcpt + detected_slope * (detected_period - 1))
end_price = np.exp(detected_intrcpt)
upper_start_price = start_price * np.exp(dev_multiplier * detected_std_dev)
upper_end_price = end_price * np.exp(dev_multiplier * detected_std_dev)
lower_start_price = start_price / np.exp(dev_multiplier * detected_std_dev)
lower_end_price = end_price / np.exp(dev_multiplier * detected_std_dev)

# Add calculated columns to the DataFrame
df['Adaptive Trend Finder (log)'] = pd.Series(highest_pearson_r).apply(confidence)


# (Optional: Add other calculated values as columns if needed)
# df['base_line_start'] = start_price
# df['base_line_end'] = end_price
# df['upper_line_start'] = upper_start_price
# df['upper_line_end'] = upper_end_price
# df['lower_line_start'] = lower_start_price
# df['lower_line_end'] = lower_end_price

# Save the DataFrame with new columns to a CSV file
df.to_csv('data.csv', index=False)
