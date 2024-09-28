def bollinger_bands(df, window=20, num_std=2):
    """
    Calculate Bollinger Bands.

    Parameters:
    df (pd.DataFrame): The DataFrame containing 'close' prices.
    window (int): The window size for the middle band (SMA).
    num_std (int): The number of standard deviations for the upper and lower bands.

    Returns:
    tuple: Middle band (SMA), upper band, lower band as pd.Series.
    """
    sma = df['close'].rolling(window=window).mean()
    std = df['close'].rolling(window=window).std()

    upper_band = sma + num_std * std
    lower_band = sma - num_std * std

    return sma, upper_band, lower_band
