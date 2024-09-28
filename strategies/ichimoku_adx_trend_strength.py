from indicators.ichimoku import ichimoku
from indicators.adx import adx


def apply_ichimoku_adx_trend_strength(dataframe, prices="mid"):
    df = dataframe.copy()
    # Calculate ADX
    df['ADX'] = adx(df, window=14)

    # Apply Ichimoku Cloud
    df['Tenkan_sen'], df['Kijun_sen'], df['Senkou_Span_A'], df['Senkou_Span_B'] = ichimoku(df)

    # Buy/Sell Signals
    df['Buy Signal'] = (df[f'{prices}_close'] > df['Senkou_Span_A']) & (df['ADX'] > 25)
    df['Sell Signal'] = (df[f'{prices}_close'] < df['Senkou_Span_B']) & (df['ADX'] > 25)
