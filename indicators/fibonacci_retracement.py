def fibonacci_retracement(df, swing_high, swing_low):
    """
    Calculate Fibonacci retracement levels based on swing high and swing low.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the 'close' prices.
    swing_high (float): The swing high price.
    swing_low (float): The swing low price.

    Returns:
    dict: A dictionary containing Fibonacci retracement levels (23.6%, 38.2%, 50%, 61.8%, 78.6%).
    """
    # Fibonacci ratios
    fibonacci_ratios = [0.236, 0.382, 0.5, 0.618, 0.786]

    # Calculate Fibonacci retracement levels
    levels = {}
    for ratio in fibonacci_ratios:
        level = swing_high - (swing_high - swing_low) * ratio
        levels[f'{int(ratio*100)}%'] = level

    return levels
