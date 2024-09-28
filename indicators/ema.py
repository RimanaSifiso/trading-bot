def calculate_ema(df, window):
    """
    Calculate the Exponential Moving Average (EMA).

    Parameters:
    df (pd.DataFrame): The DataFrame containing the 'close' prices.
    window (int): The window size for calculating the EMA.

    Returns:
    pd.Series: The EMA values as a Series.
    """
    return df['close'].ewm(span=window, adjust=False).mean()