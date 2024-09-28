import talib


def adx(df, window=14):
    """
    Calculate the Average Directional Index (ADX).

    Parameters:
    df (pd.DataFrame): The DataFrame containing 'high', 'low', 'close' prices.
    window (int): The window size for calculating the ADX (default is 14).

    Returns:
    pd.Series: ADX values.
    """
    return talib.ADX(df['high'], df['low'], df['close'], timeperiod=window)