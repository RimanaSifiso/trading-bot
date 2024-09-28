def rsi(df, window=14):
    """
    Calculate the Relative Strength Index (RSI).

    Parameters:
    df (pd.DataFrame): The DataFrame containing 'close' prices.
    window (int): The window size for calculating the RSI (default is 14).

    Returns:
    pd.Series: The RSI values.
    """
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi
