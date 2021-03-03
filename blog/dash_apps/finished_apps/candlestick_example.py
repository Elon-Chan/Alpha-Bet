import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dt
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from django_plotly_dash import DjangoDash

import pandas as pd
from datetime import datetime, date
import yfinance as yf

def today():
    return datetime.now().date()

def download_yfinance_data(ticker, start_date, end_date):
    print('downloading')
    stock = yf.Ticker(ticker)
    history = stock.history(start=start_date, end=end_date)
    return history

app = DjangoDash('Candlestick', external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Input(id='stock-ticker', type='text', value='TSLA', placeholder='TSLA'),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        month_format='D-M-Y',
        min_date_allowed=date(2010, 1, 1),
        max_date_allowed=today(),
        initial_visible_month=date(2021, 1, 1),
        start_date = date(2021,1,1),
        end_date=today()
    ),
    html.Button('Submit', id='submit_val', n_clicks=0),
    dcc.Dropdown(id='strategy-dropdown', 
             options=[{'label': 'Moving Average', 'value': 'MA'},
                      {'label': 'Relative Strength Index', 'value': 'RSI'}]),
    html.Div(id='chosen-ticker'),
    dcc.Checklist(
        id='toggle-rangeslider',
        options=[{'label': 'Include Rangeslider', 
                  'value': 'slider'}],
        value=['slider']
    ),
    dcc.Graph(id="graph"),
    dt.DataTable(id='report-table')
])

@app.callback(
    [
    Output("graph", "figure"), 
    Output("chosen-ticker", "children"),
    Output("report-table", "data"),
    Output('report-table', 'columns')
    ],
    [
    Input('submit_val', 'n_clicks'), 
    Input("toggle-rangeslider", "value"),
    ],
    [State('stock-ticker', 'value'),
     State("strategy-dropdown", 'value'),
     State('my-date-picker-range', 'start_date'), 
     State('my-date-picker-range', 'end_date'),])
def display_candlestick(n_click, slider, ticker, strategy, start_date, end_date):

    current_ticker = f"You are currently choosing {ticker} from {start_date} to {end_date}, strategy: {strategy}"
    df = download_yfinance_data(ticker, start_date, end_date)

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if strategy == 'MA':
        df['MA1'] = df['Close'].rolling(10).mean()
        df['MA2'] = df['Close'].rolling(20).mean()
        fig.add_trace(go.Scatter(x=df.index, y=df['MA1'], name='MA1'))
        fig.add_trace(go.Scatter(x=df.index, y=df['MA2'], name='MA2'))

    elif strategy == 'RSI':
        # Need to install talib, not enough space
        pass



    # include candlestick with rangeselector
    fig.add_trace(go.Candlestick(x=df.index,
                    open=df['Open'], high=df['High'],
                    low=df['Low'], close=df['Close'], name='Price'),
                secondary_y=False)

    # include a go.Bar trace for volumes
    # fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume'),
    #             secondary_y=True)

    fig.layout.yaxis2.showgrid=False

    df['Return'] = df['Close']/df['Close'].shift(1) - 1
    bnh_return = df['Return'].tail(1)
    volatility = df['Close'].std()


    columns = ['Base Return', 'Strategy Return', 'Volatility']
    data = [bnh_return, 0, volatility]
    d = {'Base Return': [bnh_return], 'Strategy Return': [0], 'Volatility': [volatility]}
    df2 = pd.DataFrame(data=d)
    print(df2)
    

    return fig, current_ticker, df2.values, df2.columns