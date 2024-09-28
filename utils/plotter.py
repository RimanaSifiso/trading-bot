import plotly.graph_objects as go
import plotly.offline as py_offline

"""
The Plotter Class is a util class that uses plotly library to plot candle data. 
"""


class Plotter:
    def __init__(self, df_candles):
        """
        Initialize the Plotter with a DataFrame containing candle data.

        :param df_candles: pd.DataFrame. The DataFrame containing OHLC data ('open', 'high', 'low', 'close')
        and optional traces (e.g., indicators like SMA, EMA).
        """
        self.df = df_candles
        # self.fig = go.Figure()

    def plot_candles(
            self,
            title="Candlestick Chart",
            prices="bid",
            traces=None,
            markers=None,
            secondary_y_traces=None
    ):
        """
        Plot the candlestick chart along with optional traces, markers, and secondary axes.

        :param title: The title of the plot
        :param prices: The prices to use for plotting the candlestick chart, should be one of bid|mid|ask
        :param traces: The traces to use for plotting the candlestick chart, could be SMA, EMA, etc.
        :param markers: The markers to use for plotting the candlestick chart, could be BUY/SELL, etc.
        :param secondary_y_traces: Option secondary y traces to use for plotting the candlestick chart, could be RSI, etc
        """
        fig = go.Figure()

        # Add candlestick chart
        fig.add_trace(go.Candlestick(
            x=self.df.timestamp,
            open=self.df[f'{prices}_open'],
            high=self.df[f'{prices}_high'],
            low=self.df[f'{prices}_low'],
            close=self.df[f'{prices}_close'],
            name='Candlesticks'
        ))

        # Plot traces on the primary axis
        if traces:
            for trace in traces:
                if trace in self.df.columns:
                    fig.add_trace(go.Scatter(
                        x=self.df.timestamp,
                        y=self.df[trace],
                        mode='lines',
                        name=trace
                    ))

        # Plot traces on the secondary axis (if provided)
        if secondary_y_traces:
            for trace in secondary_y_traces:
                if trace in self.df.columns:
                    fig.add_trace(go.Scatter(
                        x=self.df.timestamp,
                        y=self.df[trace],
                        mode='lines',
                        name=trace,
                        yaxis="y2"
                    ))
            # Add secondary axis to layout
            fig.update_layout(
                yaxis2=dict(
                    overlaying='y',
                    side='right',
                    title=trace
                )
            )

        # Plot markers (e.g., Buy/Sell signals)
        if markers:
            for marker_name, marker_series in markers.items():
                fig.add_trace(go.Scatter(
                    x=self.df.timestamp[marker_series],
                    y=self.df[f'{prices}_close'][marker_series],
                    mode='markers',
                    marker=dict(size=10),
                    name=marker_name
                ))

        # Update layout
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,  # Center the title
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20, color="black", family="Arial", style='normal')  # Normal text, no italics
            },
            xaxis=dict(
                showgrid=True,
                gridwidth=0.1,  # Tiny grid lines on x-axis
                gridcolor='gray',
                tickfont=dict(size=10, color='black', family="Arial", style='normal'),  # Smaller font for dates
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=0.01,  # Tiny grid lines on y-axis
                gridcolor='gray',
                tickfont=dict(size=10, color='black', family="Arial", style='normal'),  # Smaller font for prices
            ),
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background for the whole chart
            xaxis_title=dict(text="Date", font=dict(size=12, color="black", family="Arial", style='normal')),  # X-axis label no italics
            yaxis_title=dict(text="Price", font=dict(size=12, color="black", family="Arial", style='normal')),  # Y-axis label no italics
            template='plotly_dark',

        )

        fig.update_traces(
            increasing_line_color='green',
            decreasing_line_color='red',
            increasing_fillcolor='green',
            decreasing_fillcolor='red',
            line=dict(width=1)  # No outline/border for candles
        )

        # Show the figure
        fig.show()

