class Candle:
    def __init__(self, row, previous=None):
        """
        Initializes the Candle object from a row of the DataFrame (pd.Series).

        Parameters:
        row (pd.Series): A row from the DataFrame containing candle data.
        """
        # Basic OHLC for bid prices
        self.bid_open = row['bid_open']
        self.bid_high = row['bid_high']
        self.bid_low = row['bid_low']
        self.bid_close = row['bid_close']

        self.open = self.bid_open
        self.high = self.bid_high
        self.low = self.bid_low
        self.close = self.bid_close

        # OHLC for ask prices
        self.ask_open = row['ask_open']
        self.ask_high = row['ask_high']
        self.ask_low = row['ask_low']
        self.ask_close = row['ask_close']

        # OHLC for mid-prices (calculated from ask and bid prices if needed)
        self.mid_open = row['mid_open']
        self.mid_high = row['mid_high']
        self.mid_low = row['mid_low']
        self.mid_close = row['mid_close']

        # Volume and timestamp
        self.volume = row['volume']
        self.timestamp = row['timestamp']

        # Derived attributes
        self.body_size = abs(self.bid_open - self.bid_close)
        self.total_range = self.bid_high - self.bid_low
        self.upper_wick = self.bid_high - max(self.bid_open, self.bid_close)
        self.lower_wick = min(self.bid_open, self.bid_close) - self.bid_low
        self.body_to_range_ratio = self.body_size / self.total_range if self.total_range != 0 else 0
        self.candle_type = 'bullish' if self.bid_close > self.bid_open else 'bearish'

        self.previous = previous

    def __str__(self):
        return (f"Candle({self.candle_type}): Open={self.open}, High={self.high}, "
                f"Low={self.low}, Close={self.close}, Body Size={self.body_size}, "
                f"Upper Wick={self.upper_wick}, Lower Wick={self.lower_wick}, "
                f"Body/Range Ratio={self.body_to_range_ratio:.2f}")

    def is_spinning_top(self):
        """
        A Spinning Top has a small real body and long upper and lower shadows (wicks).
        Conditions:
        - The body size should be less than 30% of the total candle range.
        - Both the upper and lower wicks should be larger than the body size (e.g., at least twice the body size).
        """
        # Condition 1: Small body relative to total range
        small_body = self.body_to_range_ratio < 0.3

        # Condition 2: Long upper and lower shadows (wicks at least twice the body size)
        long_upper_shadow = self.upper_wick >= 2 * self.body_size
        long_lower_shadow = self.lower_wick >= 2 * self.body_size

        # Return True if all conditions for a spinning top are met
        return small_body and long_upper_shadow and long_lower_shadow

    def is_marubozu(self, tolerance=0.001):
        """
        Detects whether the candle is a Marubozu (either bullish or bearish).

        A Marubozu has no upper or lower shadows, or very small shadows within a tolerance.
        - White (Bullish) Marubozu: Open == Low and Close == High (with small tolerance for wicks).
        - Black (Bearish) Marubozu: Open == High and Close == Low (with small tolerance for wicks).

        Parameters:
        tolerance (float): Maximum allowable difference between the open/close and high/low to still be considered a Marubozu.

        Returns:
        tuple (bool, str | None): True, 'bullish_marubozu' or True, 'bearish_marubozu' if detected, otherwise False, None.
        """
        # White Marubozu: open == low and close == high (within a small tolerance)
        if abs(self.open - self.low) <= tolerance and abs(self.close - self.high) <= tolerance:
            return True, 'bullish'

        # Black Marubozu: open == high and close == low (within a small tolerance)
        elif abs(self.open - self.high) <= tolerance and abs(self.close - self.low) <= tolerance:
            return True, 'bearish'

        return False, None

    def is_doji(self, tolerance=0.001):
        """
        Detects whether the candle is a Doji (and which type).

        A Doji occurs when the open and close prices are nearly identical.
        There are four types of Doji based on the lengths of the wicks:
        - Long-Legged Doji: Long upper and lower shadows
        - Dragonfly Doji: Long lower shadow, no upper shadow
        - Gravestone Doji: Long upper shadow, no lower shadow
        - Four Price Doji: No shadows, open == close == high == low (very rare)

        Parameters:
        tolerance (float): Maximum allowable difference between the open and close to be considered a Doji.

        Returns:
        tuple (bool, str | None): True and the type of Doji ('long_legged', 'dragonfly', 'gravestone', 'four_price') if detected, otherwise False and None.
        """
        # Condition for a Doji: Open and close prices must be very close (small body)
        small_body = abs(self.open - self.close) <= tolerance

        # Check for Four Price Doji (open, close, high, and low are almost equal)
        if small_body and abs(self.high - self.low) <= tolerance:
            return True, 'four_price'

        # Check for Dragonfly Doji (long lower shadow, no upper shadow)
        if small_body and self.upper_wick <= tolerance and self.lower_wick > 2 * self.body_size:
            return True, 'dragonfly'

        # Check for Gravestone Doji (long upper shadow, no lower shadow)
        if small_body and self.lower_wick <= tolerance and self.upper_wick > 2 * self.body_size:
            return True, 'gravestone'

        # Check for Long-Legged Doji (long upper and lower shadows)
        if small_body and self.upper_wick > 2 * self.body_size and self.lower_wick > 2 * self.body_size:
            return True, 'long_legged'

        return False, None

    def is_hanging_man(self):
        """
        Detects a Hanging Man pattern.

        A Hanging Man occurs at the top of an uptrend and has:
        - A small body near the top of the candle's range.
        - A long lower shadow at least twice the size of the body.
        - Very little or no upper shadow.

        Returns:
        bool: True if a Hanging Man pattern is detected, otherwise False.
        """
        # Small body near the top and long lower shadow
        small_body = self.body_size / self.total_range <= 0.3
        long_lower_shadow = self.lower_wick > 2 * self.body_size
        very_little_upper_shadow = self.upper_wick <= 0.1 * self.body_size

        return small_body and long_lower_shadow and very_little_upper_shadow

    def is_shooting_star(self):
        """
        Detects a Shooting Star pattern.

        A Shooting Star occurs at the top of an uptrend and has:
        - A small body near the bottom of the candle's range.
        - A long upper shadow at least twice the size of the body.
        - Very little or no lower shadow.

        Returns:
        bool: True if a Shooting Star pattern is detected, otherwise False.
        """
        # Small body near the bottom and long upper shadow
        small_body = self.body_size / self.total_range <= 0.3
        long_upper_shadow = self.upper_wick > 2 * self.body_size
        very_little_lower_shadow = self.lower_wick <= 0.1 * self.body_size

        return small_body and long_upper_shadow and very_little_lower_shadow

    def is_inverted_hammer(self):
        """
        Detects an Inverted Hammer pattern.

        An Inverted Hammer occurs at the bottom of a downtrend and has:
        - A small body near the bottom of the candle's range.
        - A long upper shadow at least twice the size of the body.
        - Very little or no lower shadow.

        Returns:
        bool: True if an Inverted Hammer pattern is detected, otherwise False.
        """
        # Small body near the bottom and long upper shadow
        small_body = self.body_size / self.total_range <= 0.3
        long_upper_shadow = self.upper_wick > 2 * self.body_size
        very_little_lower_shadow = self.lower_wick <= 0.1 * self.body_size

        return small_body and long_upper_shadow and very_little_lower_shadow

    def is_shooting_star(self):
        """
        Detects a Shooting Star pattern.

        A Shooting Star occurs at the top of an uptrend and has:
        - A small body near the bottom of the candle's range.
        - A long upper shadow at least twice the size of the body.
        - Very little or no lower shadow.

        Returns:
        bool: True if a Shooting Star pattern is detected, otherwise False.
        """
        # Small body near the bottom and long upper shadow
        small_body = self.body_size / self.total_range <= 0.3
        long_upper_shadow = self.upper_wick > 2 * self.body_size
        very_little_lower_shadow = self.lower_wick <= 0.1 * self.body_size

        return small_body and long_upper_shadow and very_little_lower_shadow

    def is_hammer(self):
        """
        Detects a Hammer pattern.

        A Hammer occurs at the bottom of a downtrend and has:
        - A small body near the top of the candle's range.
        - A long lower shadow at least twice the size of the body.
        - Very little or no upper shadow.

        Returns:
        bool: True if a Hammer pattern is detected, otherwise False.
        """
        # Small body near the top and long lower shadow
        small_body = self.body_size / self.total_range <= 0.3
        long_lower_shadow = self.lower_wick > 2 * self.body_size
        very_little_upper_shadow = self.upper_wick <= 0.1 * self.body_size

        return small_body and long_lower_shadow and very_little_upper_shadow

    # TODO: Start plotting these
    def is_bullish_engulfing(self):
        """
        Detects a Bullish Engulfing pattern.

        A Bullish Engulfing pattern occurs when:
        - A bearish candle is followed by a bullish candle.
        - The body of the bullish candle completely engulfs the body of the previous bearish candle.

        Parameters:
        previous_candle (Candle): The candle immediately before the current one.

        Returns:
        bool: True if a Bullish Engulfing pattern is detected, otherwise False.
        """
        # Condition 1: Previous candle is bearish, current candle is bullish
        if self.previous.candle_type == 'bearish' and self.candle_type == 'bullish':
            # Condition 2: The body of the current (bullish) candle engulfs the previous (bearish) candle
            return self.bid_open < self.previous.bid_close and self.bid_close > self.previous.bid_open

        return False

    def is_bearish_engulfing(self):
        """
        Detects a Bearish Engulfing pattern.

        A Bearish Engulfing pattern occurs when:
        - A bullish candle is followed by a bearish candle.
        - The body of the bearish candle completely engulfs the body of the previous bullish candle.

        Parameters:
        self.previous (Candle): The candle immediately before the current one.

        Returns:
        bool: True if a Bearish Engulfing pattern is detected, otherwise False.
        """
        # Condition 1: Previous candle is bullish, current candle is bearish
        if self.previous.candle_type == 'bullish' and self.candle_type == 'bearish':
            # Condition 2: The body of the current (bearish) candle engulfs the previous (bullish) candle
            return self.bid_open > self.previous.bid_close and self.bid_close < self.previous.bid_open

        return False

    def is_tweezer_top(self, tolerance=0.001):
        """
        Detects a Tweezer Top pattern.

        A Tweezer Top occurs at the top of an uptrend and has:
        - A bullish candle followed by a bearish candle.
        - Both candles have nearly identical high prices (within a tolerance).

        Parameters:
        previous_candle (Candle): The candle immediately before the current one.
        tolerance (float): Maximum allowable difference between the high prices of the two candles.

        Returns:
        bool: True if a Tweezer Top pattern is detected, otherwise False.
        """
        # Condition 1: First candle is bullish, second candle is bearish
        if self.previous.candle_type == 'bullish' and self.candle_type == 'bearish':
            # Condition 2: The highs of both candles are nearly identical (within tolerance)
            return abs(self.bid_high - self.previous.bid_high) <= tolerance

        return False

    def is_tweezer_bottom(self, tolerance=0.001):
        """
        Detects a Tweezer Bottom pattern.

        A Tweezer Bottom occurs at the bottom of a downtrend and has:
        - A bearish candle followed by a bullish candle.
        - Both candles have nearly identical low prices (within a tolerance).

        Parameters:
        previous_candle (Candle): The candle immediately before the current one.
        tolerance (float): Maximum allowable difference between the low prices of the two candles.

        Returns:
        bool: True if a Tweezer Bottom pattern is detected, otherwise False.
        """
        # Condition 1: First candle is bearish, second candle is bullish
        if self.previous.candle_type == 'bearish' and self.candle_type == 'bullish':
            # Condition 2: The lows of both candles are nearly identical (within tolerance)
            return abs(self.bid_low - self.previous.bid_low) <= tolerance

        return False

    def is_bullish_harami(self):
        """
        Detects a Bullish Harami pattern.

        A Bullish Harami occurs when:
        - A large bearish candle is followed by a smaller bullish candle.
        - The body of the second (bullish) candle is completely contained within the body of the first (bearish) candle.

        Parameters:
        previous_candle (Candle): The candle immediately before the current one.

        Returns:
        bool: True if a Bullish Harami pattern is detected, otherwise False.
        """
        if self.previous.candle_type == 'bearish' and self.candle_type == 'bullish':
            return self.bid_open > self.previous.bid_close and self.bid_close < self.previous.bid_open
        return False

    def is_bearish_harami(self):
        """
        Detects a Bearish Harami pattern.

        A Bearish Harami occurs when:
        - A large bullish candle is followed by a smaller bearish candle.
        - The body of the second (bearish) candle is completely contained within the body of the first (bullish) candle.

        Parameters:
        previous_candle (Candle): The candle immediately before the current one.

        Returns:
        bool: True if a Bearish Harami pattern is detected, otherwise False.
        """
        if self.previous.candle_type == 'bullish' and self.candle_type == 'bearish':
            return self.bid_open < self.previous.bid_close and self.bid_close > self.previous.bid_open
        return False

    def is_piercing_pattern(self):
        """
        Detects a Piercing Pattern.

        A Piercing Pattern occurs when:
        - A bearish candle is followed by a bullish candle.
        - The second candle opens below the low of the first candle and closes more than halfway up the body of the first candle.

        Parameters:
        previous_candle (Candle): The candle immediately before the current one.

        Returns:
        bool: True if a Piercing Pattern is detected, otherwise False.
        """
        if self.previous.candle_type == 'bearish' and self.candle_type == 'bullish':
            halfway_point = (self.previous.bid_open + self.previous.bid_close) / 2
            return self.bid_open < self.previous.bid_low and self.bid_close > halfway_point
        return False

    def is_dark_cloud_cover(self):
        """
        Detects a Dark Cloud Cover pattern.

        A Dark Cloud Cover occurs when:
        - A bullish candle is followed by a bearish candle.
        - The second candle opens above the high of the first candle and closes more than halfway into the body of the first candle.

        Parameters:
        previous_candle (Candle): The candle immediately before the current one.

        Returns:
        bool: True if a Dark Cloud Cover pattern is detected, otherwise False.
        """
        if self.previous.candle_type == 'bullish' and self.candle_type == 'bearish':
            halfway_point = (self.previous.bid_open + self.previous.bid_close) / 2
            return self.bid_open > self.previous.bid_high and self.bid_close < halfway_point
        return False

    def is_matching_high(self, tolerance=0.001):
        """
        Detects a Matching High pattern.

        A Matching High occurs when two consecutive candles have nearly identical high prices.

        Parameters:
        previous_candle (Candle): The candle immediately before the current one.
        tolerance (float): Maximum allowable difference between the high prices of the two candles.

        Returns:
        bool: True if a Matching High pattern is detected, otherwise False.
        """
        return abs(self.bid_high - self.previous.bid_high) <= tolerance

    def is_matching_low(self, tolerance=0.001):
        """
        Detects a Matching Low pattern.

        A Matching Low occurs when two consecutive candles have nearly identical low prices.

        Parameters:
        previous_candle (Candle): The candle immediately before the current one.
        tolerance (float): Maximum allowable difference between the low prices of the two candles.

        Returns:
        bool: True if a Matching Low pattern is detected, otherwise False.
        """
        return abs(self.bid_low - self.previous.bid_low) <= tolerance

    def is_bullish_kicker(self):
        """
        Detects a Bullish Kicker pattern.

        A Bullish Kicker occurs when:
        - A bearish candle is followed by a bullish candle with a gap up.
        - The second candle opens above the open of the first candle and shows strong bullish momentum.

        Parameters:
        previous_candle (Candle): The candle immediately before the current one.

        Returns:
        bool: True if a Bullish Kicker pattern is detected, otherwise False.
        """
        return self.previous.candle_type == 'bearish' and self.candle_type == 'bullish' and self.bid_open > self.previous.bid_open

    def is_bearish_kicker(self):
        """
        Detects a Bearish Kicker pattern.

        A Bearish Kicker occurs when:
        - A bullish candle is followed by a bearish candle with a gap down.
        - The second candle opens below the open of the first candle and shows strong bearish momentum.

        Parameters:
        previous_candle (Candle): The candle immediately before the current one.

        Returns:
        bool: True if a Bearish Kicker pattern is detected, otherwise False.
        """
        return self.previous.candle_type == 'bullish' and self.candle_type == 'bearish' and self.bid_open < self.previous.bid_open

    def is_inside_bar(self):
        """
        Detects an Inside Bar pattern.

        An Inside Bar occurs when the high and low of the second candle are within the high and low of the previous candle.

        Parameters:
        previous_candle (Candle): The candle immediately before the current one.

        Returns:
        bool: True if an Inside Bar pattern is detected, otherwise False.
        """
        return self.bid_high < self.previous.bid_high and self.bid_low > self.previous.bid_low

    # three candlestick patterns
    def is_morning_star(self):
        """
        Detects a Morning Star pattern.

        A Morning Star is a three-candlestick pattern signaling a bullish reversal.
        - The first candle is a large bearish candle.
        - The second candle is a smaller candle that signals indecision (bullish or bearish).
        - The third candle is a large bullish candle that closes beyond the midpoint of the first candle.

        Parameters:
        self.previous_1 (Candle): The first candle in the pattern (before the current one).
        self.previous_2 (Candle): The second candle in the pattern (before the previous one).

        Returns:
        bool: True if a Morning Star pattern is detected, otherwise False.
        """
        # Condition 1: The first candle is bearish (continuing the downtrend)
        if self.previous.previous.candle_type == 'bearish':
            # Condition 2: The second candle has a small body (indecision)
            small_body = abs(self.previous.bid_open - self.previous.bid_close) / self.previous.total_range <= 0.3

            # Condition 3: The third candle is bullish and closes beyond the midpoint of the first candle
            midpoint = (self.previous.previous.bid_open + self.previous.previous.bid_close) / 2
            if small_body and self.candle_type == 'bullish' and self.bid_close > midpoint:
                return True

        return False

    def is_evening_star(self):
        """
        Detects an Evening Star pattern.

        An Evening Star is a three-candlestick pattern signaling a bearish reversal.
        - The first candle is a large bullish candle.
        - The second candle is a smaller candle that signals indecision (bullish or bearish).
        - The third candle is a large bearish candle that closes beyond the midpoint of the first candle.

        Parameters:
        self.previous (Candle): The first candle in the pattern (before the current one).
        self.previous.previous (Candle): The second candle in the pattern (before the previous one).

        Returns:
        bool: True if an Evening Star pattern is detected, otherwise False.
        """
        # Condition 1: The first candle is bullish (continuing the uptrend)
        if self.previous.previous.candle_type == 'bullish':
            # Condition 2: The second candle has a small body (indecision)
            small_body = abs(self.previous.bid_open - self.previous.bid_close) / self.previous.total_range <= 0.3

            # Condition 3: The third candle is bearish and closes beyond the midpoint of the first candle
            midpoint = (self.previous.previous.bid_open + self.previous.previous.bid_close) / 2
            if small_body and self.candle_type == 'bearish' and self.bid_close < midpoint:
                return True

        return False

    def is_three_white_soldiers(self):
        """
        Detects a Three White Soldiers pattern.

        The Three White Soldiers pattern signals a strong bullish reversal after a downtrend.
        - The first candle is a bullish reversal candle.
        - The second candle is a bullish candle larger than the first, with a close near the high and little or no upper shadow.
        - The third candle is another bullish candle, at least the same size as the second, with little or no shadow.

        Parameters:
        self.previous (Candle): The candle before the current one.
        self.previous.previous (Candle): The candle two periods before the current one.

        Returns:
        bool: True if a Three White Soldiers pattern is detected, otherwise False.
        """
        if self.previous.previous.candle_type == 'bullish' and self.previous.candle_type == 'bullish' and self.candle_type == 'bullish':
            # Condition 1: The second candle is larger than the first and closes near its high
            second_candle_conditions = self.previous.bid_close > self.previous.previous.bid_close and \
                                       self.previous.bid_close > self.previous.bid_open and \
                                       (self.previous.bid_high - self.previous.bid_close) <= (self.previous.total_range * 0.1)

            # Condition 2: The third candle is at least the same size as the second and has a small or no shadow
            third_candle_conditions = self.bid_close > self.bid_open and \
                                      (self.bid_high - self.bid_close) <= (self.total_range * 0.1) and \
                                      self.total_range >= self.previous.total_range

            return second_candle_conditions and third_candle_conditions

        return False

    def is_three_black_crows(self):
        """
        Detects a Three Black Crows pattern.

        The Three Black Crows pattern signals a strong bearish reversal after an uptrend.
        - The first candle is a bearish reversal candle.
        - The second candle is a bearish candle larger than the first, with a close near the low and little or no lower shadow.
        - The third candle is another bearish candle, at least the same size as the second, with little or no shadow.

        Parameters:
        self.previous (Candle): The candle before the current one.
        self.previous.previous (Candle): The candle two periods before the current one.

        Returns:
        bool: True if a Three Black Crows pattern is detected, otherwise False.
        """
        if self.previous.previous.candle_type == 'bearish' and self.previous.candle_type == 'bearish' and self.candle_type == 'bearish':
            # Condition 1: The second candle is larger than the first and closes near its low
            second_candle_conditions = self.previous.bid_close < self.previous.previous.bid_close and \
                                       self.previous.bid_close < self.previous.bid_open and \
                                       (self.previous.bid_close - self.previous.bid_low) <= (self.previous.total_range * 0.1)

            # Condition 2: The third candle is at least the same size as the second and has a small or no shadow
            third_candle_conditions = self.bid_close < self.bid_open and \
                                      (self.bid_close - self.bid_low) <= (self.total_range * 0.1) and \
                                      self.total_range >= self.previous.total_range

            return second_candle_conditions and third_candle_conditions

        return False

    def is_three_inside_up(self):
        """
        Detects a Three Inside Up pattern.

        The Three Inside Up pattern signals a bullish reversal after a downtrend.
        - The first candle is a long bearish candle.
        - The second candle is a bullish candle that reaches or exceeds the midpoint of the first candle.
        - The third candle is a bullish candle that closes above the high of the first candle, confirming the reversal.

        Parameters:
        self.previous (Candle): The candle before the current one.
        self.previous.previous (Candle): The candle two periods before the current one.

        Returns:
        bool: True if a Three Inside Up pattern is detected, otherwise False.
        """
        if self.previous.previous.candle_type == 'bearish' and self.previous.candle_type == 'bullish' and self.candle_type == 'bullish':
            # Condition 1: The second candle must reach or exceed the midpoint of the first candle
            midpoint = (self.previous.previous.bid_open + self.previous.previous.bid_close) / 2
            second_candle_conditions = self.previous.bid_close > midpoint

            # Condition 2: The third candle must close above the first candle's high
            third_candle_conditions = self.bid_close > self.previous.previous.bid_high

            return second_candle_conditions and third_candle_conditions

        return False

    def is_three_inside_down(self):
        """
        Detects a Three Inside Down pattern.

        The Three Inside Down pattern signals a bearish reversal after an uptrend.
        - The first candle is a long bullish candle.
        - The second candle is a bearish candle that reaches or exceeds the midpoint of the first candle.
        - The third candle is a bearish candle that closes below the low of the first candle, confirming the reversal.


        Returns:
        bool: True if a Three Inside Down pattern is detected, otherwise False.
        """
        if self.previous.candle_type == 'bullish' and self.previous.candle_type == 'bearish' and self.candle_type == 'bearish':
            # Condition 1: The second candle must reach or exceed the midpoint of the first candle
            midpoint = (self.previous.previous.bid_open + self.previous.previous.bid_close) / 2
            second_candle_conditions = self.previous.bid_close < midpoint

            # Condition 2: The third candle must close below the first candle's low
            third_candle_conditions = self.bid_close < self.previous.previous.bid_low

            return second_candle_conditions and third_candle_conditions

        return False

    def is_three_outside_up(self):
        """
        Detects a Three Outside Up pattern (bullish reversal).

        The Three Outside Up pattern signals a strong bullish reversal after a downtrend.
        - The first candle is a bearish candle.
        - The second candle is a bullish candle that engulfs the first candle.
        - The third candle is another bullish candle that closes higher than the second.

        Returns:
        bool: True if a Three Outside Up pattern is detected, otherwise False.
        """
        if self.previous and self.previous.previous:
            first_candle = self.previous.previous
            second_candle = self.previous

            # Check for bullish engulfing (second candle engulfs first)
            if first_candle.candle_type == 'bearish' and second_candle.candle_type == 'bullish':
                engulfing = second_candle.bid_open < first_candle.bid_close and second_candle.bid_close > first_candle.bid_open
                third_candle_confirmation = self.candle_type == 'bullish' and self.bid_close > second_candle.bid_close

                return engulfing and third_candle_confirmation

        return False

    def is_three_outside_down(self):
        """
        Detects a Three Outside Down pattern (bearish reversal).

        The Three Outside Down pattern signals a strong bearish reversal after an uptrend.
        - The first candle is a bullish candle.
        - The second candle is a bearish candle that engulfs the first candle.
        - The third candle is another bearish candle that closes lower than the second.

        Returns:
        bool: True if a Three Outside Down pattern is detected, otherwise False.
        """
        if self.previous and self.previous.previous:
            first_candle = self.previous.previous
            second_candle = self.previous

            # Check for bearish engulfing (second candle engulfs first)
            if first_candle.candle_type == 'bullish' and second_candle.candle_type == 'bearish':
                engulfing = second_candle.bid_open > first_candle.bid_close and second_candle.bid_close < first_candle.bid_open
                third_candle_confirmation = self.candle_type == 'bearish' and self.bid_close < second_candle.bid_close

                return engulfing and third_candle_confirmation

        return False

    def is_bullish_abandoned_baby(self):
        """
        Detects a Bullish Abandoned Baby pattern (bullish reversal).

        The Bullish Abandoned Baby pattern signals a strong bullish reversal after a downtrend.
        - The first candle is a bearish candle.
        - The second candle is a Doji with a gap down from the first candle.
        - The third candle is a bullish candle with a gap up from the Doji.

        Returns:
        bool: True if a Bullish Abandoned Baby pattern is detected, otherwise False.
        """
        if self.previous and self.previous.previous:
            first_candle = self.previous.previous
            second_candle = self.previous

            # Check for a Doji with a gap down and a gap up
            if first_candle.candle_type == 'bearish' and abs(second_candle.bid_open - second_candle.bid_close) <= (second_candle.total_range * 0.1):
                gap_down = second_candle.bid_open < first_candle.bid_low
                gap_up = self.bid_open > second_candle.bid_high
                return gap_down and gap_up and self.candle_type == 'bullish'

        return False

    def is_bearish_abandoned_baby(self):
        """
        Detects a Bearish Abandoned Baby pattern (bearish reversal).

        The Bearish Abandoned Baby pattern signals a strong bearish reversal after an uptrend.
        - The first candle is a bullish candle.
        - The second candle is a Doji with a gap up from the first candle.
        - The third candle is a bearish candle with a gap down from the Doji.

        Returns:
        bool: True if a Bearish Abandoned Baby pattern is detected, otherwise False.
        """
        if self.previous and self.previous.previous:
            first_candle = self.previous.previous
            second_candle = self.previous

            # Check for a Doji with a gap up and a gap down
            if first_candle.candle_type == 'bullish' and abs(second_candle.bid_open - second_candle.bid_close) <= (second_candle.total_range * 0.1):
                gap_up = second_candle.bid_open > first_candle.bid_high
                gap_down = self.bid_open < second_candle.bid_low
                return gap_up and gap_down and self.candle_type == 'bearish'

        return False

    def is_bullish_three_line_strike(self):
        """
        Detects a Bullish Three Line Strike pattern.

        The Bullish Three Line Strike pattern signals a bullish reversal.
        - The first three candles are bearish, each closing lower than the previous one.
        - The fourth candle is bullish and closes above the open of the first bearish candle.

        Returns:
        bool: True if a Bullish Three Line Strike pattern is detected, otherwise False.
        """
        if self.previous and self.previous.previous and self.previous.previous.previous:
            first_candle = self.previous.previous.previous
            second_candle = self.previous.previous
            third_candle = self.previous

            if first_candle.candle_type == 'bearish' and second_candle.candle_type == 'bearish' and third_candle.candle_type == 'bearish':
                # Check if each candle closes lower than the previous one
                if second_candle.bid_close < first_candle.bid_close and third_candle.bid_close < second_candle.bid_close:
                    # Check if the current (fourth) candle is bullish and closes above the open of the first candle
                    return self.candle_type == 'bullish' and self.bid_close > first_candle.bid_open

        return False

    def is_bearish_three_line_strike(self):
        """
        Detects a Bearish Three Line Strike pattern.

        The Bearish Three Line Strike pattern signals a bearish reversal.
        - The first three candles are bullish, each closing higher than the previous one.
        - The fourth candle is bearish and closes below the open of the first bullish candle.

        Returns:
        bool: True if a Bearish Three Line Strike pattern is detected, otherwise False.
        """
        if self.previous and self.previous.previous and self.previous.previous.previous:
            first_candle = self.previous.previous.previous
            second_candle = self.previous.previous
            third_candle = self.previous

            if first_candle.candle_type == 'bullish' and second_candle.candle_type == 'bullish' and third_candle.candle_type == 'bullish':
                # Check if each candle closes higher than the previous one
                if first_candle.bid_close < second_candle.bid_close < third_candle.bid_close:
                    # Check if the current (fourth) candle is bearish and closes below the open of the first candle
                    return self.candle_type == 'bearish' and self.bid_close < first_candle.bid_open

        return False
