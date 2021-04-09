# dash related libraries
from typing import Dict
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_html_components.Div import Div
import dash_table as dt
from dash.dependencies import Input, Output, State, ALL
from numpy.lib.function_base import append

# plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# django plotly dash
from django_plotly_dash import DjangoDash

# my own code
from .technical_indicators import dropdown_options, compute_technical_indicators, dictionary_buy_1, dictionary_buy_2, dictionary_sell_1, dictionary_sell_2

# data processing
import pandas as pd
from datetime import datetime, date
import yfinance as yf
import talib

def today():
    return datetime.now().date()

def download_yfinance_data(ticker, start_date, end_date):
    print('downloading')
    stock = yf.Ticker(ticker)
    history = stock.history(start=start_date, end=end_date)
    return history

def compute_bnh_performance(df):
    
    pct_return = round((df['Close'].iloc[-1] / df['Close'].iloc[0] - 1) * 100, 4)
    volatility = round(df['Close'].std(), 4)

    roll_max = df['Close'].rolling(window=252, min_periods=1).max()
    daily_drawdown = (df['Close']/roll_max - 1) * 100
    mdd = round(daily_drawdown.min(), 4)

    sharpe = round(pct_return/volatility, 4)
    return [pct_return, volatility, mdd, sharpe]

def compute_strategy_performance(df):
    pass

app = DjangoDash('strategy_analyzer')

app.layout = html.Div([
    html.H1(children="Stock Strategy Analyzer", style={'text-align':'center'}),
    html.Div(children=[
        html.P(children="Please Input Your Stock Ticker: ", style={'display': 'inline-block'}),
        dcc.Input(id='stock-ticker', type='text', value='TSLA', placeholder='TSLA', style={'display': 'inline-block'}),
        ]),
    html.Div(children=[
        html.P(children="Please Choose the Desired Date Range: ", style={'display': 'inline-block'}),
        dcc.DatePickerRange(
            id='my-date-picker-range',
            month_format='D-M-Y',
            min_date_allowed=date(2010, 1, 1),
            max_date_allowed=today(),
            initial_visible_month=date(2021, 1, 1),
            start_date = date(2021,1,1),
            end_date=today(),
            style={'display': 'inline-block'}),
    ]),
    
    html.Div(children=[
        html.H3(children="If"),
        dcc.Dropdown(id='buy-strategy-1', 
            options=dropdown_options,
            value='MA'),
        html.Div(id='buy-strategy-1-parameter-container'),
        html.H3(children="Cross Up"),
        dcc.Dropdown(id='buy-strategy-2', 
            options=dropdown_options,
            value='MA'),
        html.Div(id='buy-strategy-2-parameter-container'),
        html.H3(children="Then Buy"),
    ], style={'width': '25%'}),

    html.Div(children=[
        html.H3(children="If"),
        dcc.Dropdown(id='sell-strategy-1', 
            options=dropdown_options,
            value='MA'),
        html.Div(id='sell-strategy-1-parameter-container'),
        html.H3(children="Cross Up"),
        dcc.Dropdown(id='sell-strategy-2', 
            options=dropdown_options,
            value='MA'),
        html.Div(id='sell-strategy-2-parameter-container'),
        html.H3(children="Then Sell"),
    ], style={'width': '25%'}),

    html.Div(children=[html.Button('Submit', id='submit-val', n_clicks=0)], style={'text-align':'center'}),

    html.Div(id='input-log'), # For information reporting, dev only
    dcc.Checklist(
        id='toggle-rangeslider',
        options=[{'label': 'Include Rangeslider', 
                    'value': 'slider'}],
        value=['slider']
    ),
    dcc.Graph(id="graph"),

    html.Div(children=[
        html.H4(children='Performance Report'),
        html.Table(
            children=[
                html.Tr(children=[
                    html.Th(),
                    html.Th(children='Return'),
                    html.Th(children='Volatility'),
                    html.Th(children='Maximum Drawdown'),
                    html.Th(children='Sharpe Ratio'),
                ]),
                html.Tr(children=[
                    html.Th(children='Buy and Hold'),
                    html.Td(id='bnh-Return', children='10%'),
                    html.Td(id='bnh-Volatility', children='273%'),
                    html.Td(id='bnh-Maximum Drawdown', children='28%'),
                    html.Td(id='bnh-Sharpe Ratio', children='0.89'),
                ]),
                html.Tr(children=[
                    html.Th(children='Strategy'),
                    html.Td(id='Return', children='10%'),
                    html.Td(id='Volatility', children='273%'),
                    html.Td(id='Maximum Drawdown', children='28%'),
                    html.Td(id='Sharpe Ratio', children='0.89'),
                ]),
            ]
        )
    ],
    )
])

@app.callback(
    [
        Output('input-log', 'children'),
        Output('graph', 'figure'),
        Output('bnh-Return', 'children'),
        Output('bnh-Volatility', 'children'),
        Output('bnh-Maximum Drawdown', 'children'),
        Output('bnh-Sharpe Ratio', 'children'),
    ],
    [
        Input('submit-val', 'n_clicks'),
        Input("toggle-rangeslider", "value"),
    ],
    [
        State('stock-ticker', 'value'),
        State('my-date-picker-range', 'start_date'), 
        State('my-date-picker-range', 'end_date'),
        State('buy-strategy-1', 'value'),
        State({'type':'buy-strategy-1-parameter-value', 'index': ALL}, 'value'),
        State('buy-strategy-2', 'value'),
        State({'type':'buy-strategy-2-parameter-value', 'index': ALL}, 'value'),
        State('sell-strategy-1', 'value'),
        State({'type':'sell-strategy-1-parameter-value', 'index': ALL}, 'value'),
        State('sell-strategy-2', 'value'),
        State({'type':'sell-strategy-2-parameter-value', 'index': ALL}, 'value'),
    ]
)
def display_graph(n_clicks, slider, ticker, start_date, end_date, buy_strategy_1, buy_strategy_1_parameter_value, buy_strategy_2, buy_strategy_2_parameter_value, sell_strategy_1, sell_strategy_1_parameter_value, sell_strategy_2, sell_strategy_2_parameter_value):

    if n_clicks == 0: 
        raise dash.exceptions.PreventUpdate

    debug_log = str(buy_strategy_1_parameter_value) + str(buy_strategy_2_parameter_value) + str(sell_strategy_1_parameter_value) + str(sell_strategy_2_parameter_value)
    print(debug_log)

    df = download_yfinance_data(ticker, start_date, end_date)

    buy_technical_indicators = compute_technical_indicators(df, buy_strategy_1, buy_strategy_1_parameter_value, buy_strategy_2, buy_strategy_2_parameter_value)
    sell_technical_indicators = compute_technical_indicators(df, sell_strategy_1, sell_strategy_1_parameter_value, sell_strategy_2, sell_strategy_2_parameter_value)
    
    print(buy_technical_indicators, sell_technical_indicators)

    bnh_performance = compute_bnh_performance(df)
    # strategy_performance = compute_strategy_performance(df, buy_strategy_1, buy_strategy_1_parameter, buy_strategy_2, buy_strategy_2_parameter)

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=buy_technical_indicators[0].index, y=buy_technical_indicators[0].values))
    fig.add_trace(go.Scatter(x=buy_technical_indicators[1].index, y=buy_technical_indicators[1].values))

    fig.add_trace(go.Candlestick(x=df.index,
            open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'], name='Price'),
        secondary_y=False)

    fig.update_layout(xaxis_rangeslider_visible='slider' in slider)

    
    return [debug_log, fig, bnh_performance[0], bnh_performance[1], bnh_performance[2], bnh_performance[3]]



@app.callback(
    [
        Output('buy-strategy-1-parameter-container', 'children'),
        Output('buy-strategy-2-parameter-container', 'children'),
        Output('sell-strategy-1-parameter-container', 'children'),
        Output('sell-strategy-2-parameter-container', 'children'),
    ],
    [
        Input('buy-strategy-1', 'value'),
        Input('buy-strategy-2', 'value'),
        Input('sell-strategy-1', 'value'),
        Input('sell-strategy-2', 'value'),
    ],
    )
def display_inputs(buy_strategy_1_value, buy_strategy_2_value, sell_strategy_1_value, sell_strategy_2_value):
    print(buy_strategy_1_value, buy_strategy_2_value, sell_strategy_1_value, sell_strategy_2_value)

    buy_strategy_1_parameter = dictionary_buy_1[buy_strategy_1_value]
    buy_strategy_2_parameter = dictionary_buy_2[buy_strategy_2_value]
    sell_strategy_1_parameter = dictionary_sell_1[sell_strategy_1_value]
    sell_strategy_2_parameter = dictionary_sell_2[sell_strategy_2_value]

    return [buy_strategy_1_parameter, buy_strategy_2_parameter, sell_strategy_1_parameter, sell_strategy_2_parameter]