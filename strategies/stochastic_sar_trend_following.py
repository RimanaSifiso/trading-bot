
from indicators.parabolic_sar import parabolic_sar
from indicators.stochastic import stochastic


def apply_stochastic_trend_following(dataframe, prices="mid"):
    df = dataframe.copy()
    df['Parabolic_SAR'] = parabolic_sar(df)
    df['%K'], df['%D'] = stochastic(df)
    # Buy/Sell Signals based on Stochastic and Parabolic SAR
    df['Buy Signal'] = (df['%K'] < 20) & (df['%K'] > df['%D']) & (df['Parabolic_SAR'] < df[f'{prices}_close'])
    df['Sell Signal'] = (df['%K'] > 80) & (df['%K'] < df['%D']) & (df['Parabolic_SAR'] > df[f'{prices}_close'])
