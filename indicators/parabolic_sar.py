import talib


def parabolic_sar(df):
    """
    Calculate Parabolic SAR.

    Parameters:
    df (pd.DataFrame): The DataFrame containing 'high' and 'low' prices.

    Returns:
    pd.Series: Parabolic SAR values.
    """
    return talib.SAR(df['high'], df['low'], acceleration=0.02, maximum=0.2)
