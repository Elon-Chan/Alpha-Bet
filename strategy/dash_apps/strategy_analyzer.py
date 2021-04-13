# dash related libraries
from typing import Dict
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash_html_components.Div import Div
import dash_table as dt
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State, ALL
from numpy.lib.function_base import append

# plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# django plotly dash
from django_plotly_dash import DjangoDash

# my own code
from .technical_indicators import dropdown_options, compute_technical_indicators, create_input

# data processing
import pandas as pd
import numpy as np
from datetime import datetime, date
import yfinance as yf
import talib


def blank_figure():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None, paper_bgcolor = 'rgba(0,0,0,0)',
                    plot_bgcolor = 'rgba(0,0,0,0)')
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    
    return fig


def today():
    return datetime.now().date()

def download_yfinance_data(ticker, start_date, end_date):
    print('downloading')
    stock = yf.Ticker(ticker)
    history = stock.history(start=start_date, end=end_date)
    return history

def compute_bnh_performance(df):
    pct_return = round((df['Close'].iloc[-1] / df['Close'].iloc[0] - 1) * 100, 2)
    volatility = round(df['Close'].std(), 2)

    roll_max = df['Close'].cummax()
    daily_drawdown = (df['Close']/roll_max - 1) * 100
    mdd = round(daily_drawdown.cummin()[-1], 2)

    sharpe = round(pct_return/volatility, 2)
    return [pct_return, volatility, mdd, sharpe]

def compute_strategy_performance(df, buy_technical_indicators, sell_technical_indicators):
    
    pct_return = (df['Close'] / df['Close'].shift(1) - 1)
    
    buy = np.where(buy_technical_indicators[0] > buy_technical_indicators[1], 1, 0)
    buy_return = buy * pct_return
    
    sell = np.where(sell_technical_indicators[0] > sell_technical_indicators[1], -1, 0)
    sell_return = sell * pct_return

    overall_return = 1 + buy_return + sell_return
    overall_return.dropna(inplace=True)

    strategy_return = round((overall_return.cumprod()[-1] - 1)*100, 2)
    
    traded_day_price = (buy + (-1 * sell)) * df['Close']
    traded_day_price = traded_day_price[traded_day_price != 0]
    volatility = round(traded_day_price.std(), 2)

    roll_max = traded_day_price.cummax()
    daily_drawdown = (traded_day_price/roll_max - 1) * 100
    mdd = round(daily_drawdown.cummin()[-1], 2)

    sharpe = round(strategy_return/volatility, 2)

    return [strategy_return, volatility, mdd, sharpe]


app = DjangoDash('strategy_analyzer', add_bootstrap_links=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

disclaim = 'The content of this webpage is not an investment advice and does not constitute any offer or solicitation to offer or recommendation of any investment product. It is for general purposes only and does not take into account your individual needs, investment objectives and specific financial circumstances. Investment involves risk. The investor type classification has no relationship with and is not any substitute for the Financial Needs Analysis (the “FNA”) or your risk profiling under the FNA. You instruct us that if there is any conflict or inconsistency between the investor type classification and your investment risk profiling under the FNA, the latter shall prevail and be used for assessing your risk profile for your conducting investment product transaction with our Bank. Please also note that asset allocation does not generate positive return or protection against market loss.'


app.layout = html.Div(children=[
    # title
    html.H1(children="Stock Strategy Analyzer", style={'text-align': 'center', 'font-family': 'HaextPlain'}),
    html.Br(),
    html.H3(children="Inform, Improve, Inexorable", style={'text-align': 'center'}),
    # linebreak
    html.Br(),
    dbc.Row(
        [
            # input ticker
            dbc.Col(
                html.Div(children=[
                    html.P(children="Please Input Your Stock Ticker: ", style={'display': 'inline-block'}),
                    dcc.Input(id='stock-ticker', type='text', value='TSLA', placeholder='TSLA', style={'display': 'inline-block'}),
                ]),
                width={"order": "first"},
            ),
            # input date
            dbc.Col(
                html.Div(children=[
                    html.P(children="Please Choose the Desired Date Range: ", style={'display': 'inline-block'}),
                    dcc.DatePickerRange(
                        id='my-date-picker-range',
                        month_format='D-M-Y',
                        min_date_allowed=date(2010, 1, 1),
                        max_date_allowed=today(),
                        initial_visible_month=date(2021, 1, 1),
                        start_date=date(2021, 1, 1),
                        end_date=today(),
                        style={'display': 'inline-block'}),
                ]),
                width={"order": "last"},
            ),
        ],
        style={"text-align": "center"},
    ),

    html.Br(),

    # card deck
    dbc.Row(
        [
            dbc.Col([
                html.Div(children=[
                    dbc.Card([
                        dbc.CardHeader([html.H2(children="Buy")]),
                        dbc.CardBody([
                            html.H3(children="If"),
                            dcc.Dropdown(id='buy-strategy-1',
                                            options=dropdown_options,
                                            value='MA',
                                            style={"color": "#000", 'font-size': '15px',}),
                            html.Div(id='buy-strategy-1-parameter-container', style={'padding-top': '10px'}),
                            html.H3(children="Cross Up", style={'padding-top': '5px'}),
                            dcc.Dropdown(id='buy-strategy-2',
                                            options=dropdown_options,
                                            value='MA',
                                            style={"color": "#000", 'font-size': '15px',}),
                            html.Div(id='buy-strategy-2-parameter-container', style={'padding-top': '10px'}),
                        ]),
                    ],
                        color="#5c5c5c",
                        inverse=True,
                        style={"width": "35rem"},
                    ),
                ]),
            ], width="auto"),
            dbc.Col([
                html.Div(children=[
                    dbc.Card([
                        dbc.CardHeader([html.H2(children="Sell")]),
                        dbc.CardBody([
                            html.H3(children="If"),
                            dcc.Dropdown(id='sell-strategy-1',
                                            options=dropdown_options,
                                            value='MA',
                                            style={"color": "#000", 'font-size': '15px',}),
                            html.Div(id='sell-strategy-1-parameter-container', style={'padding-top': '10px'}),
                            html.H3(children="Cross Up", style={'padding-top': '5px'}),
                            dcc.Dropdown(id='sell-strategy-2',
                                            options=dropdown_options,
                                            value='MA',
                                            style={"color": "#000", 'font-size': '15px',}),
                            html.Div(id='sell-strategy-2-parameter-container', style={'padding-top': '10px'}),
                        ]),
                    ],
                        color="#5c5c5c",
                        inverse=True,
                        style={"width": "35rem"},
                    ),
                ]),
            ], width="auto"),
        ],
        justify="between"
    ),

    # linebreak
    html.Br(),

    # submit button
    html.Div(
        children=[dbc.Button(
            'Analyze', id='submit-val',
            n_clicks=0,
            outline=True,
            color="primary",
            className="mr-1",
            style={
                "font-size": "25px",
                'color': 'white',
                'font-family': 'HaextPlain',
                'font-weight': 'bold',
                "padding": "5px 80px 10px",
                "border-radius": "6px",
            }
        )],
        style={'text-align': 'center'}
    ),

    # linebreak
    html.Br(),

    # For information reporting, dev only
    html.Div(id='input-log'),

    # result
    html.Div([
        dbc.Card(
            dbc.CardHeader(
                html.H3("Stock Trend and Strategy Movements")
            ),
            color="#5c5c5c",
            inverse=True,
        ),
        dbc.Card(
            dbc.CardBody(
                dcc.Graph(id="graph", figure=blank_figure()),
            ),
            color="#48484a",
            inverse=True,
        ),
        dbc.Card(
            dbc.CardHeader(
                dcc.Checklist(
                    id='toggle-rangeslider',
                    options=[{'label': 'Include Rangeslider', 'value': 'slider'}],
                    value=['slider'],
                    style={'font-family': 'AspergitRegular'}
                ),
            ),
            color="#5c5c5c",
            inverse=True,
        ),
    ]),

    # linebreak
    html.Br(),
    html.Br(),

    # performance report
    dbc.Card(
        dbc.CardHeader(
            html.H3("Performance Report")
        ),
        color="#5c5c5c",
        inverse=True,
    ),
    dbc.Row([
        dbc.Col(dbc.Card(
            dbc.CardBody([
                html.Table(
                    children=[
                        html.Tr(children=[
                            html.Th(children='  Buy And Hold', colSpan='4', style={'font-family': 'AspergitRegular', 'font-size': '30px', 'text-align': 'left', 'padding-left':'10px'}),
                        ]),
                        html.Tr(children=[
                            html.Td(children='Return(%)', style={'border': '1px solid #ddd', 'border-collapse': 'collapse', 'padding': '7px', 'font-family': 'AspergitRegular', 'font-size': '15px'}),
                            html.Td(children='Volatility', style={'border': '1px solid #ddd', 'border-collapse': 'collapse', 'padding': '7px', 'font-family': 'AspergitRegular', 'font-size': '15px'}),
                            html.Td(children='Maximum Drawdown(%)', style={'border': '1px solid #ddd', 'border-collapse': 'collapse', 'padding': '7px', 'font-family': 'AspergitRegular', 'font-size': '15px'}),
                            html.Td(children='Sharpe Ratio', style={'border': '1px solid #ddd', 'border-collapse': 'collapse', 'padding': '7px', 'font-family': 'AspergitRegular', 'font-size': '15px'}),
                        ], style={'padding-left':'10px'}),
                        html.Tr(children=[
                            html.Td(id='bnh-Return', children=[], style={'border': '1px solid #ddd', 'border-collapse': 'collapse', 'colspan': '3', 'font-size': '15px'}),
                            html.Td(id='bnh-Volatility', children=[], style={'border': '1px solid #ddd', 'border-collapse': 'collapse', 'font-size': '15px'}),
                            html.Td(id='bnh-Maximum Drawdown', children=[], style={'border': '1px solid #ddd', 'border-collapse': 'collapse', 'font-size': '15px'}),
                            html.Td(id='bnh-Sharpe Ratio', children=[], style={'border': '1px solid #ddd', 'border-collapse': 'collapse', 'font-size': '15px'}),
                        ], style={'padding-left':'10px'}),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Tr(children=[
                            html.Th(children='  Strategy', colSpan='4', style={'font-family': 'AspergitRegular', 'font-size': '30px', 'text-align': 'left','padding-left':'10px'}),
                        ]),
                        html.Tr(children=[
                            html.Td(children='Return(%)', style={'border': '1px solid #ddd', 'border-collapse': 'collapse', 'padding': '7px', 'font-family': 'AspergitRegular', 'font-size': '15px'}),
                            html.Td(children='Volatility', style={'border': '1px solid #ddd', 'border-collapse': 'collapse', 'padding': '7px', 'font-family': 'AspergitRegular', 'font-size': '15px'}),
                            html.Td(children='Maximum Drawdown(%)', style={'border': '1px solid #ddd', 'border-collapse': 'collapse', 'padding': '7px', 'font-family': 'AspergitRegular', 'font-size': '15px'}),
                            html.Td(children='Sharpe Ratio', style={'border': '1px solid #ddd', 'border-collapse': 'collapse', 'padding': '7px', 'font-family': 'AspergitRegular', 'font-size': '15px'}),
                        ], style={'padding-left':'100px'}),
                        html.Tr(children=[
                            html.Td(id='Return', children=[], style={'border': '1px solid #ddd', 'border-collapse': 'collapse', 'font-size': '15px'}),
                            html.Td(id='Volatility', children=[], style={'border': '1px solid #ddd', 'border-collapse': 'collapse', 'font-size': '15px'}),
                            html.Td(id='Maximum Drawdown', children=[], style={'border': '1px solid #ddd', 'border-collapse': 'collapse', 'font-size': '15px'}),
                            html.Td(id='Sharpe Ratio', children=[], style={'border': '1px solid #ddd', 'border-collapse': 'collapse', 'font-size': '15px'}),
                        ], style={'margin-left':'100px'}),
                    ]
                ),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Div(id='disclaimer', children=f'Disclaimer: {disclaim}', style={'font-size': '10px'}),
            ]
            ),
            color="#48484a",
            inverse=True,
        ), width=5
        ),
        dbc.Col(dbc.Card(
            dbc.CardBody(
                dcc.Graph(id="radar", figure=blank_figure()),
            ),
            color="#48484a",
            inverse=True
        ), width=7
        ),
    ]),
])

@app.callback(
    [
        Output('input-log', 'children'),
        Output('graph', 'figure'),
        Output('bnh-Return', 'children'),
        Output('bnh-Volatility', 'children'),
        Output('bnh-Maximum Drawdown', 'children'),
        Output('bnh-Sharpe Ratio', 'children'),
        Output('Return', 'children'),
        Output('Volatility', 'children'),
        Output('Maximum Drawdown', 'children'),
        Output('Sharpe Ratio', 'children'),
        Output('radar', 'figure'),
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

    df = download_yfinance_data(ticker, start_date, end_date)
    buy_technical_indicators = compute_technical_indicators(df, buy_strategy_1, buy_strategy_1_parameter_value, buy_strategy_2, buy_strategy_2_parameter_value)
    sell_technical_indicators = compute_technical_indicators(df, sell_strategy_1, sell_strategy_1_parameter_value, sell_strategy_2, sell_strategy_2_parameter_value)

    bnh_performance = compute_bnh_performance(df)
    strategy_performance = compute_strategy_performance(df, buy_technical_indicators, sell_technical_indicators)

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=buy_technical_indicators[0].index, y=buy_technical_indicators[0].values))
    fig.add_trace(go.Scatter(x=buy_technical_indicators[1].index, y=buy_technical_indicators[1].values))
    fig.add_trace(go.Scatter(x=sell_technical_indicators[0].index, y=sell_technical_indicators[0].values))
    fig.add_trace(go.Scatter(x=sell_technical_indicators[1].index, y=sell_technical_indicators[1].values))

    fig.add_trace(go.Candlestick(x=df.index,
            open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'], name='Price'),
        secondary_y=False)

    fig.update_layout(xaxis_rangeslider_visible='slider' in slider, paper_bgcolor = 'rgba(0,0,0,0)',
                    plot_bgcolor = 'rgba(0,0,0,0)')

    categories = ['Return', 'Volatility', 'Maximum Drawdown', 'Sharpe Ratio']
    radar = make_subplots(specs=[[{"secondary_y": True}]])

    radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=False,
                range=[1, 5]
            )
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        autosize=True,
        font=dict(
            size=20,
            color='white',
            family='AspergitRegular'
            )
    )

    benchmark = [1, 20, 5, 0.5]
    bnh_performance_rate = []
    strategy_performance_rate = []

    for i, (bnh_quality, strategy_quality) in enumerate(zip(bnh_performance, strategy_performance)):
        print(bnh_quality, strategy_quality)
        bnh_ratio = np.abs(bnh_quality)/benchmark[i] - 1
        print(bnh_ratio)
        strategy_ratio = np.abs(strategy_quality)/benchmark[i] - 1
        if bnh_ratio < 0:
            bnh_performance_rate.append(1)
        elif bnh_ratio >= 0 and bnh_ratio < 5:
            bnh_performance_rate.append(2)
        elif bnh_ratio >= 5 and bnh_ratio < 10:
            bnh_performance_rate.append(3)
        elif bnh_ratio >= 10 and bnh_ratio < 15:
            bnh_performance_rate.append(4)
        elif bnh_ratio >= 15:
            bnh_performance_rate.append(5)

        if strategy_ratio < 0:
            strategy_performance_rate.append(1)
        elif strategy_ratio >= 0 and bnh_ratio < 5:
            strategy_performance_rate.append(2)
        elif strategy_ratio >= 5 and bnh_ratio < 10:
            strategy_performance_rate.append(3)
        elif strategy_ratio >= 10 and bnh_ratio < 15:
            strategy_performance_rate.append(4)
        elif strategy_ratio >= 15:
            strategy_performance_rate.append(5)

    radar.add_trace(go.Scatterpolar(
        r=[strategy_performance_rate[0], strategy_performance_rate[1], strategy_performance_rate[2], strategy_performance_rate[3]],
        theta=categories,
        fill='toself',
        name='Strategy'
    ))  
    radar.add_trace(go.Scatterpolar(
        r=[bnh_performance_rate[0], bnh_performance_rate[1], bnh_performance_rate[2], bnh_performance_rate[3]],
        theta=categories,
        fill='toself',
        name='Buy and Hold'
    ))



    
    return [debug_log, fig, bnh_performance[0], bnh_performance[1], bnh_performance[2], bnh_performance[3], strategy_performance[0], strategy_performance[1], strategy_performance[2], strategy_performance[3], radar]

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
def display_inputs(buy_strategy_1, buy_strategy_2, sell_strategy_1, sell_strategy_2):

    buy_strategy_1_parameter = create_input(buy_strategy_1, 'buy', '1')
    buy_strategy_2_parameter = create_input(buy_strategy_2, 'buy', '2')
    sell_strategy_1_parameter = create_input(sell_strategy_1, 'sell', '1')
    sell_strategy_2_parameter = create_input(sell_strategy_2, 'sell', '2')

    return [buy_strategy_1_parameter, buy_strategy_2_parameter, sell_strategy_1_parameter, sell_strategy_2_parameter]