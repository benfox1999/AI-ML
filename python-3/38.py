import pandas as pd
import numpy as np
import talib

def colorize(power, originalColorScheme=True):
    """Heatmap Color Helper Function (not used directly, for reference)"""
    red = 255
    grn = 0
    if power > 0.5:
        grn = int(510.0 * (power - 0.5))
    else:
        red = int(510.0 * power)
    # Color logic not relevant for data processing, omitted

def hp1st(series, period):
    """John Ehlers' 1st Order High Pass Filter"""
    afreq = 2.0 * np.pi / period
    coef1 = (1.0 - np.sin(afreq)) / np.cos(afreq)
    coef0 = (1.0 + coef1) * 0.5
    mom = series.diff()
    hp = np.zeros_like(series)
    hp[1:] = coef0 * mom[1:] + coef1 * hp[:-1]
    return hp

def hp2nd(series, period):
    """John Ehlers' 2nd Order High Pass Filter"""
    afreq = np.sqrt(2.0) * np.pi / period
    alpha = (np.cos(afreq) + np.sin(afreq) - 1.0) / np.cos(afreq)
    coef0 = (1.0 - alpha / 2.0)**2
    coef1 = (1.0 - alpha) * 2.0
    coef2 = (1.0 - alpha)**2
    whiten = series.diff(2)
    hp = np.zeros_like(series)
    hp[2:] = coef0 * whiten[2:] + coef1 * hp[1:-1] - coef2 * hp[:-2]
    return hp


def sups(series, period):
    """John Ehlers' SuperSmoother Function"""
    
    # Convert the input series to a Pandas Series if it's not already one
    if not isinstance(series, pd.Series):
        series = pd.Series(series)
    
    if len(series) < 2 or period < 2.0:
        return series.copy()

    afreq = np.sqrt(2.0) * np.pi / period
    alpha = np.exp(-afreq)
    coef2 = -alpha**2
    coef1 = np.cos(afreq) * 2.0 * alpha
    coef0 = 1.0 - coef1 - coef2

    sma2 = (series + series.shift(1)).rolling(2).mean()
    smooth = pd.Series(np.nan, index=series.index) 
    smooth[2:] = coef0 * sma2[2:] + coef1 * smooth.shift(1)[2:] + coef2 * smooth.shift(2)[2:]

    return smooth


def roof(series, low_pass_period=7.5, high_pass_period=49, high_pass_selection=True):
    """Custom Roofing Filter"""
    if high_pass_selection:
        return sups(hp2nd(series, high_pass_period), low_pass_period)
    else:
        return sups(hp1st(series, high_pass_period), low_pass_period)

def acs(passband_series, auto_correlation_lag=3, power_threshold=0.05,
        contrast=3.0, fourier_filt_algo='ESS', fourier_filt_period=10):
    """AutoCorrelation Spectrum Function"""
    auto_correlation_lag_m1 = auto_correlation_lag - 1
    a_fourier_factors = np.zeros(50)
    m_smoothing_coefs = np.zeros((50, 3))
    
    # Precalculate Coefficients and Fourier Factors
    for p in range(6, 50):
        if fourier_filt_algo == 'ESS':
            afreq = np.sqrt(2.0) * np.pi / min(p, fourier_filt_period)
            alpha = np.exp(-afreq)
            m_smoothing_coefs[p] = [1.0 - 2*alpha*np.cos(afreq) - alpha**2, 2*alpha*(1 + np.cos(afreq)), -alpha**2]
        else:
            coef0 = 2.0 / (fourier_filt_period + 1)
            m_smoothing_coefs[p] = [coef0, 1.0 - coef0, 0]
        a_fourier_factors[p] = 2.0 * np.pi / p

    passband_series2 = passband_series**2
    a_auto_correlations_r = np.zeros(50)
    
    # Calculate AutoCorrelations
    for p in range(50):
        ex = ey = exy = exx = eyy = 0.0
        for i in range(auto_correlation_lag_m1 + 1):
            t = i + p
            X = passband_series.iloc[i] if i < len(passband_series) else 0
            Y = passband_series.iloc[t] if t < len(passband_series) else 0
            ex  += X
            exy += X * Y
            ey  += Y
            exx += passband_series2.iloc[i] if i < len(passband_series2) else 0
            eyy += passband_series2.iloc[t] if t < len(passband_series2) else 0
        
        denominator = (auto_correlation_lag * exx - ex**2) * (auto_correlation_lag * eyy - ey**2)
        if denominator > 0.0:
            a_auto_correlations_r[p] = (auto_correlation_lag * exy - ex * ey) / np.sqrt(denominator)
    
    a_spectral_comps = np.zeros(50)
    
    # Decompose Fourier Components
    for p in range(6, 50):
        real_part = imag_part = 0.0
        angular_freq_factor = a_fourier_factors[p]
        for i in range(50):
            real_part += np.cos(angular_freq_factor * i) * a_auto_correlations_r[i]
            imag_part += np.sin(angular_freq_factor * i) * a_auto_correlations_r[i]
        a_spectral_comps[p] = real_part**2 + imag_part**2
    
    a_smoothed_fourier_comps = np.zeros(50)
    
    if fourier_filt_algo == 'ESS':
        # Fourier Components SuperSmoothed
        a_smoothed_fourier_comps[6] = a_spectral_comps[6]
        a_smoothed_fourier_comps[7] = m_smoothing_coefs[7, 0] * a_spectral_comps[7] + m_smoothing_coefs[7, 1] * a_smoothed_fourier_comps[6]
        for p in range(8, 50):
            a_smoothed_fourier_comps[p] = m_smoothing_coefs[p, 0] * a_spectral_comps[p] + \
                                         m_smoothing_coefs[p, 1] * a_smoothed_fourier_comps[p - 1] + \
                                         m_smoothing_coefs[p, 2] * a_smoothed_fourier_comps[p - 2]
    elif fourier_filt_algo == 'EMA':
        # Fourier Components EMA Smoothed
        a_smoothed_fourier_comps[6] = a_spectral_comps[6]
        for p in range(7, 50):
            a_smoothed_fourier_comps[p] = m_smoothing_coefs[p, 0] * a_spectral_comps[p] + \
                                         m_smoothing_coefs[p, 1] * a_smoothed_fourier_comps[p - 1]
    else:
        # 'NONE'
        a_smoothed_fourier_comps = a_spectral_comps.copy()
    
    peak_power = np.max(a_smoothed_fourier_comps[6:])
    if peak_power == 0:
        peak_power = 1e-10
    dividend = divisor = 0.0
    
    # Determine Dominant Cycle Period
    for p in range(6, 50):
        # Now peak_power is guaranteed to be non-zero
        spectri_normalized = (a_smoothed_fourier_comps[p] / peak_power)**contrast  

        if spectri_normalized > power_threshold:
            dividend += spectri_normalized * p
            divisor  += spectri_normalized
        a_spectral_comps[p] = spectri_normalized  # Reassign normalized spectral components
    
    dominant_cycle = 7
    if divisor > 0.25:
        dominant_cycle = max(7, dividend / divisor)
    
    return dominant_cycle, a_spectral_comps

# Load data from CSV
df = pd.read_csv('data.csv')

# Configuration (matching Pine Script inputs)
select_source_or_sine = 'Source'  # 'Source' or 'SineWave'
source_column = 'hlcc4'           # Replace with your desired source column
sine_wave_period = 16.0
roofing_filter_lp = 7.5
roofing_filter_hp = 49
highpass_selection = True
auto_correlation_lag = 3
fourier_coefs_filter = 'ESS'     # 'ESS', 'EMA', 'NONE'
fourier_smooth_period = 9
power_threshold = 0.05
heat_map_contrast = 2.5
heat_map_color_scheme = True      # Not used for calculation
dominant_cycle_type = 'Float'      # 'Float' or 'Integer*'
dominant_cycle_form = 'Smoothed'  # 'Smoothed', 'Floor*', 'Round*'
smooth_dominant_cycle = 7.0

# Calculate 'hlcc4' if using it as source (assuming typical OHLC data)
if source_column == 'hlcc4':
    df['hlcc4'] = (df['high'] + df['low'] + df['close'] + df['close']) / 4

# Prepare price data
if select_source_or_sine == 'Source':
    price = df[source_column] * 10.0
else:
    price = np.sin(np.arange(len(df)) * 6.2831853 / sine_wave_period) * 21.0 + 28.0

# Apply Roofing Filter
roofing_filter = roof(price, roofing_filter_lp, roofing_filter_hp, highpass_selection)

# Calculate Dominant Cycle and Spectral Power Estimates
dominant_cycle, a_spectral_power_estimates = acs(roofing_filter, auto_correlation_lag,
                                                   power_threshold, heat_map_contrast,
                                                   fourier_coefs_filter, fourier_smooth_period)

# Apply Dominant Cycle Type and Form
if dominant_cycle_type == 'Integer*':
    if dominant_cycle_form == 'Round*':
        dominant_cycle = np.round(dominant_cycle).astype(int)
    else:  # 'Floor*'
        dominant_cycle = np.floor(dominant_cycle).astype(int)
else:  # 'Float'
    if dominant_cycle_form == 'Smoothed':
        dominant_cycle = np.maximum(7.0, sups(pd.Series(dominant_cycle), smooth_dominant_cycle))
    elif dominant_cycle_form == 'Round*':
        dominant_cycle = np.round(dominant_cycle)
    else:  # 'Floor*'
        dominant_cycle = np.floor(dominant_cycle)

# Add results to DataFrame
df['[Excalibur] Ehlers AutoCorrelation Periodogram Modified'] = dominant_cycle

# Save the updated DataFrame to CSV
df.to_csv('data.csv', index=False)
