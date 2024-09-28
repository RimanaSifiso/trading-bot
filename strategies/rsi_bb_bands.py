from indicators.rsi import rsi
from indicators.bb_bands import bollinger_bands


def apply_rsi_bb_bands(dataframe, prices="mid"):
    df = dataframe.copy()
    # Apply indicators
    df['RSI'] = rsi(df)
    df['SMA'], df['Upper Band'], df['Lower Band'] = bollinger_bands(df)

    # Define buy/sell signals
    df['Buy Signal'] = (df['RSI'] < 30) & (df[f'{prices}_close'] < df['Lower Band'])
    df['Sell Signal'] = (df['RSI'] > 70) & (df[f'{prices}_close'] > df['Upper Band'])

    return df
