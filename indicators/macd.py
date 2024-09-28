def macd(df, short_window=12, long_window=26, signal_window=9):
    """
    Calculate the MACD and Signal Line.

    Parameters:
    df (pd.DataFrame): The DataFrame containing 'close' prices.
    short_window (int): The window size for the short-term EMA (default is 12).
    long_window (int): The window size for the long-term EMA (default is 26).
    signal_window (int): The window size for the signal line (default is 9).

    Returns:
    tuple: MACD line and Signal line as pd.Series.
    """
    short_ema = df['close'].ewm(span=short_window, adjust=False).mean()
    long_ema = df['close'].ewm(span=long_window, adjust=False).mean()

    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()

    return macd, signal