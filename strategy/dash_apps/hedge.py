import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
import plotly.express as px

import pandas as pd
import yfinance as yf
# django plotly dash
from django_plotly_dash import DjangoDash

app = DjangoDash('hedge')

app.layout = html.Div([
    html.Button("Add Stock", id="add-stock", n_clicks=0),
    html.Div(id='input-container', children=[]),
    html.Div(id='dropdown-container-output'),
    html.Button("Hedge", id="hedge", n_clicks=0),
    dcc.Graph(id="pie-chart"),
    html.Div(id='portfolio-beta')
])

@app.callback(
    Output('input-container', 'children'),
    [Input('add-stock', 'n_clicks')],
    [State('input-container', 'children')])
def display_inputs(n_clicks, children):
    new_input = [
        dcc.Input(
            id = {
                'type': 'stock-tickers',
                'index': n_clicks
            },
            type='text',
            placeholder='Enter a Ticker'
        ),
        dcc.Input(
        id = {
                'type': 'num-shares',
                'index': n_clicks
            },
            type='number',
            placeholder='Number of Shares',
        )
    ]

    children.append(new_input[0])
    children.append(new_input[1])
    children.append(html.Br())
    return children

@app.callback(
    [
        Output("pie-chart", "figure"),
        Output('portfolio-beta', 'children'),
    ],
    [
        Input("hedge", "n_clicks"),
    ],
    [
        State({'type': 'stock-tickers', 'index': ALL}, 'value'),
        State({'type': 'num-shares', 'index': ALL}, 'value'),
    ])
def generate_chart(n_clicks, stock_tickers, num_shares):
    if n_clicks == 0: 
        raise dash.exceptions.PreventUpdate

    stock_beta = []
    stock_price = []
    for ticker in stock_tickers:
        stock = yf.Ticker(ticker)
        stock_info = stock.info
        beta = stock.info['beta']

        if beta == None:
            beta = stock_info['beta3Year']

        stock_beta.append(beta)

        todays_data = stock.history(period='1d')
        todays_price = todays_data['Close'][0]
        stock_price.append(todays_price)

    temp = [x * y for (x, y) in zip(stock_price, num_shares)]
    portfolio_size = sum(temp)
    individual_stock_weight = temp / portfolio_size

    portfolio_beta = sum([x * y for (x, y) in zip(stock_beta, individual_stock_weight)])
    print(portfolio_beta)
    df = pd.DataFrame(data=list(zip(stock_tickers, individual_stock_weight)), columns=['Tickers', 'Weight'])
    fig = px.pie(df, values=individual_stock_weight, names=stock_tickers, title='Your Portfolio Formation')

    required_size = portfolio_size / 3 * portfolio_beta
    # get inverse instructmetns data
    SPXU = yf.Ticker('SPXU')
    SPXU_price = SPXU.history(period='1d')['Close'][0]

    required_inverse_stock = required_size/SPXU_price


    return fig, required_inverse_stock
