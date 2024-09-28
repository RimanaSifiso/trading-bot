def stochastic(df, k_window=14, d_window=3):
    """
    Calculate the Stochastic Oscillator.

    Parameters:
    df (pd.DataFrame): The DataFrame containing 'high', 'low', and 'close' prices.
    k_window (int): The window size for calculating %K.
    d_window (int): The window size for calculating %D (SMA of %K).

    Returns:
    tuple: %K and %D values as pd.Series.
    """
    highest_high = df['high'].rolling(window=k_window).max()
    lowest_low = df['low'].rolling(window=k_window).min()

    k_percent = 100 * (df['close'] - lowest_low) / (highest_high - lowest_low)
    d_percent = k_percent.rolling(window=d_window).mean()

    return k_percent, d_percent