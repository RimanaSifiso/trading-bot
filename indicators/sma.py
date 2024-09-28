def calculate_sma(df, window):
    """
    Calculate the Simple Moving Average (SMA).

    Parameters:
    df (pd.DataFrame): The DataFrame containing the 'close' prices.
    window (int): The window size for calculating the SMA.

    Returns:
    pd.Series: The SMA values as a Series.
    """
    return df['close'].rolling(window=window).mean()