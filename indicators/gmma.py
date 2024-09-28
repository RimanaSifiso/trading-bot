def calculate_gmma(df):
    """
    Calculate the Guppy Multiple Moving Averages (GMMA).

    GMMA consists of two sets of exponential moving averages (EMAs):
    - Short-term EMAs: 3, 5, 8, 10, 12, 15 periods
    - Long-term EMAs: 30, 35, 40, 45, 50, 60 periods

    Parameters:
    df (pd.DataFrame): The DataFrame containing the 'close' prices.

    Returns:
    dict: A dictionary containing the short-term and long-term GMMA EMAs as Series.
    """
    short_windows = [3, 5, 8, 10, 12, 15]
    long_windows = [30, 35, 40, 45, 50, 60]

    short_emas = {f'EMA_{window}': df['close'].ewm(span=window, adjust=False).mean() for window in short_windows}
    long_emas = {f'EMA_{window}': df['close'].ewm(span=window, adjust=False).mean() for window in long_windows}

    return {'short_term': short_emas, 'long_term': long_emas}
