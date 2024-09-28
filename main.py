import pandas as pd
import ast

from utils.plotter import Plotter

usd_jpy_url = "C:\\Users\\LENOVO\\Videos\\Projects\\Algo_Trading_Course\\simulation\\data\\candles\\2021_2024\\USD_JPY_H1.csv"
eur_usd_url = "C:\\Users\\LENOVO\\Videos\\Projects\\Algo_Trading_Course\\simulation\\data\candles\\2021_2024\\EUR_USD_H1.csv"
df_usd_jpy = pd.read_csv(usd_jpy_url).drop(["Unnamed: 0", "complete"], axis=1)


def extract_prices(dataframe):
    df = dataframe.copy()

    # first convert from string to dictionary
    df['bid'] = df['bid'].apply(ast.literal_eval)
    df['mid'] = df['mid'].apply(ast.literal_eval)
    df['ask'] = df['ask'].apply(ast.literal_eval)
    df['timestamp'] = pd.to_datetime(df['time'])
    # Extract the 'o', 'h', 'l', 'c' from the 'bid' column
    df['bid_open'] = df['bid'].apply(lambda x: float(x['o']))
    df['bid_high'] = df['bid'].apply(lambda x: float(x['h']))
    df['bid_low'] = df['bid'].apply(lambda x: float(x['l']))
    df['bid_close'] = df['bid'].apply(lambda x: float(x['c']))

    # Extract the 'o', 'h', 'l', 'c' from the 'ask' column
    df['ask_open'] = df['ask'].apply(lambda x: float(x['o']))
    df['ask_high'] = df['ask'].apply(lambda x: float(x['h']))
    df['ask_low'] = df['ask'].apply(lambda x: float(x['l']))
    df['ask_close'] = df['ask'].apply(lambda x: float(x['c']))

    # Extract the 'o', 'h', 'l', 'c' from the 'mid' column
    df['mid_open'] = df['mid'].apply(lambda x: float(x['o']))
    df['mid_high'] = df['mid'].apply(lambda x: float(x['h']))
    df['mid_low'] = df['mid'].apply(lambda x: float(x['l']))
    df['mid_close'] = df['mid'].apply(lambda x: float(x['c']))

    df.drop(['bid', 'ask', 'mid'], axis=1, inplace=True)

    return df


df_processed = extract_prices(df_usd_jpy)

plotter = Plotter(df_processed.iloc[:100].copy())
plotter.plot_candles()
