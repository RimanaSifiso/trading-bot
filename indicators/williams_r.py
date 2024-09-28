def williams_r(df, window=14):
    """
    Calculate Williams %R.

    Parameters:
    df (pd.DataFrame): The DataFrame containing 'high', 'low', and 'close' prices.
    window (int): The window size for calculating %R.

    Returns:
    pd.Series: Williams %R values.
    """
    highest_high = df['high'].rolling(window=window).max()
    lowest_low = df['low'].rolling(window=window).min()

    williams_r = (highest_high - df['close']) / (highest_high - lowest_low) * -100

    return williams_r
