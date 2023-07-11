# data_visualization.py

import plotly.graph_objects as go
import pandas as pd

def create_market_trend_figure():
    # Load your data
    data = pd.read_csv('C:/Users/Alex/Downloads/TR_clean.csv')

    # Convert 'instance_date' column to datetime
    data['instance_date'] = pd.to_datetime(data['instance_date'])

    # Group by month and calculate the average property value
    monthly_average_price = data.resample('M', on='instance_date')['price'].mean()

    # Group by month and count the number of transactions
    monthly_transactions = data.resample('M', on='instance_date').size()

    # Group by week and count the number of transactions
    weekly_transactions = data.resample('W', on='instance_date').size()

    # Create a trace for the average monthly property value
    trace1 = go.Scatter(
        x = monthly_average_price.index,
        y = monthly_average_price,
        mode = 'lines',
        name = 'Average Monthly Property Value',
        line = dict(color = 'blue')
    )

    # Create a trace for the number of monthly transactions
    trace2 = go.Bar(
        x = monthly_transactions.index,
        y = monthly_transactions,
        name = 'Number of Monthly Transactions',
        yaxis = 'y2',
        marker = dict(color = 'gray', opacity = 0.3)
    )

    # Create a trace for the number of weekly transactions
    trace3 = go.Bar(
        x = weekly_transactions.index,
        y = weekly_transactions,
        name = 'Number of Weekly Transactions',
        yaxis = 'y2',
        marker = dict(color = 'green', opacity = 0.3)
    )

    data = [trace1, trace2, trace3]

    layout = go.Layout(
        title = 'Average Monthly Property Value and Number of Transactions',
        yaxis = dict(title = 'Average Property Value'),
        yaxis2 = dict(title = 'Number of Transactions', overlaying = 'y', side = 'right')
    )

    fig = go.Figure(data = data, layout = layout)
    
    # Convert the figure to JSON
    plot_json = fig.to_json()

    return plot_json
