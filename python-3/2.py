import pandas as pd
import numpy as np


def calculate_indicators(df, output, direction):
    # Calculate gap
    df["gap"] = df["open"] / df["close"].shift(1) - 1.0

    # Use .loc for safer assignments
    df.loc[
        (output == "Opening Gaps") & (direction == "Upward") & (df["gap"] > 0), "pullback"
    ] = df["low"] / df["open"] - 1.0
    df.loc[
        (output == "Opening Gaps") & (direction == "Downward") & (df["gap"] < 0), "pullback"
    ] = df["high"] / df["open"] - 1.0

    # Combine conditions for close_vs_open calculation
    mask_upward = (output == "Opening Gaps") & (df["gap"] > 0)
    mask_downward = (output == "Opening Gaps") & (df["gap"] < 0)
    df.loc[mask_upward | mask_downward, "close_vs_open"] = (
        df["close"] / df["open"] - 1.0
    )

    # Handle 'Extreme Closes' (similar logic)
    mask_upward = (output == "Extreme Closes") & (df["close"] > df["close"].shift(1))
    mask_downward = (output == "Extreme Closes") & (df["close"] < df["close"].shift(1))
    df.loc[mask_upward | mask_downward, "pullback"] = (
        df["open"] / df["close"].shift(1) - 1.0
    )
    df.loc[mask_upward | mask_downward, "close_vs_open"] = (
        df["close"] / df["close"].shift(1) - 1.0
    )

    # Frequency Calculation (set observed=False explicitly)
    df["frequency"] = df.groupby(
        pd.cut(df["gap"].abs(), bins=[0, 0.01, 0.03, 0.05, 0.07, 0.09, 0.11, np.inf]),
        observed=False,
    )["gap"].transform("count")

    return df


# Load data from CSV
df = pd.read_csv("data.csv")

# Calculate indicators for each combination
df = calculate_indicators(df.copy(), "Opening Gaps", "Upward")
df = calculate_indicators(df.copy(), "Opening Gaps", "Downward")
df = calculate_indicators(df.copy(), "Extreme Closes", "Upward")
df = calculate_indicators(df.copy(), "Extreme Closes", "Downward")

# Save the DataFrame back to 'data.csv'
df.to_csv("data.csv", index=False)
