import numpy as np
import pandas as pd


def detect_support_resistance(df, timeframe_start, timeframe_end, tolerance=0.001, window=5):
    """
    Detect support and resistance zones in a candlestick dataset.

    :param df: candlestick dataset
    :param timeframe_start: start time of the candlestick dataset
    :param timeframe_end: end time of the candlestick dataset
    :param tolerance: The tolerance level for grouping swing highs/lows.
        Closer points within this range are treated as part of the same zone.
    :param window: The window size for grouping swing highs/lows. Larger windows capture broader trends.

    :return: support and resistance zones as a list
    """
    # Filter data for the given timeframe
    # Convert the input timeframe to timezone-aware (in UTC)
    timeframe_start = pd.to_datetime(timeframe_start).tz_localize('UTC')
    timeframe_end = pd.to_datetime(timeframe_end).tz_localize('UTC')

    df_filtered = df[(df['timestamp'] >= timeframe_start) & (df['timestamp'] <= timeframe_end)]
    if len(df_filtered) == 0:
        return None

    # Initialize lists to hold potential support and resistance levels
    support_levels = []
    resistance_levels = []

    # Detect Swing Highs and Swing Lows (Peaks and Troughs)
    for i in range(window, len(df_filtered) - window):
        high_price = df_filtered['bid_high'].iloc[i]
        low_price = df_filtered['bid_low'].iloc[i]

        # Check if it's a swing high
        if high_price == max(df_filtered['bid_high'].iloc[i-window:i+window+1]):
            resistance_levels.append(high_price)

        # Check if it's a swing low
        if low_price == min(df_filtered['bid_low'].iloc[i-window:i+window+1]):
            support_levels.append(low_price)

    # Function to aggregate nearby levels within a certain tolerance
    def aggregate_levels(levels, tolerance):
        levels = sorted(levels)
        aggregated_levels = []
        level_group = [levels[0]]

        for price in levels[1:]:
            if abs(price - np.mean(level_group)) <= tolerance * price:
                level_group.append(price)
            else:
                aggregated_levels.append(np.mean(level_group))
                level_group = [price]

        aggregated_levels.append(np.mean(level_group))
        return aggregated_levels

    # Aggregate the detected swing highs and swing lows into zones
    resistance_zones = aggregate_levels(resistance_levels, tolerance)
    support_zones = aggregate_levels(support_levels, tolerance)

    return support_zones, resistance_zones
