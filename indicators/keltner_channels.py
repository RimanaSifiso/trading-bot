def keltner_channels(df, ema_window=20, atr_window=10, multiplier=2):
    """
    Calculate Keltner Channels.

    Parameters:
    df (pd.DataFrame): The DataFrame containing 'high', 'low', 'close' prices.
    ema_window (int): The window size for the EMA (default is 20).
    atr_window (int): The window size for the Average True Range (ATR).
    multiplier (int):

 The multiplier for the ATR to calculate the channel width.

    Returns:
    tuple: Middle (EMA), upper, and lower bands as pd.Series.
    """
    ema = df['close'].ewm(span=ema_window, adjust=False).mean()
    atr = df['high'].rolling(window=atr_window).max() - df['low'].rolling(window=atr_window).min()

    upper_band = ema + (atr * multiplier)
    lower_band = ema - (atr * multiplier)

    return ema, upper_band, lower_band