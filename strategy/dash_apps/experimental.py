import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL

from django_plotly_dash import DjangoDash

# app = dash.Dash(__name__, suppress_callback_exceptions=True)
app = DjangoDash('experimental')

app.layout = html.Div([
    html.Div(children=[
        html.H3(children="If"),
        dcc.Dropdown(id='buy-strategy-1', 
            options=[{'label': 'Moving Average', 'value': 'MA'},
                    {'label': 'Relative Strength Index', 'value': 'RSI'}],
            value='MA'),
        html.Div(id='buy-strategy-1-parameter-container', children=[]),
        html.H3(children="Cross Up"),
        dcc.Dropdown(id='buy-strategy-2', 
            options=[{'label': 'Moving Average', 'value': 'MA'},
                    {'label': 'Relative Strength Index', 'value': 'RSI'}],
            value='MA'),
        html.Div(id='buy-strategy-2-parameter-container', children=[]),
        html.H3(children="Then Buy"),
    ], style={'width': '25%'}),

    html.Div(children=[
        html.H3(children="If"),
        dcc.Dropdown(id='sell-strategy-1', 
            options=[{'label': 'Moving Average', 'value': 'MA'},
                    {'label': 'Relative Strength Index', 'value': 'RSI'}],
            value='MA'),
        html.Div(id='sell-strategy-1-parameter-container', children=[]),
        html.H3(children="Cross Up"),
        dcc.Dropdown(id='sell-strategy-2', 
            options=[{'label': 'Moving Average', 'value': 'MA'},
                    {'label': 'Relative Strength Index', 'value': 'RSI'}],
            value='MA'),
        html.Div(id='sell-strategy-2-parameter-container', children=[]),
        html.H3(children="Then Sell"),
    ], style={'width': '25%'}),

    html.Div(children=[html.Button('Submit', id='submit-val', n_clicks=0)], style={'text-align':'center'}),

    html.Div(id='input-log', children='Hello World')
])

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
    print(buy_strategy_1_value, buy_strategy_2_value)
    dictionary_buy_1 = {
        'MA': dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='text', persistence=True),
        'RSI': [dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='text', persistence=True), dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':1}, type='text', persistence=True)]
    }
    dictionary_buy_2 = {
        'MA': dcc.Input(id={'type':'buy-strategy-2-parameter-value', 'index':0}, type='text', persistence=True),
        'RSI': [dcc.Input(id={'type':'buy-strategy-2-parameter-value', 'index':0}, type='text', persistence=True), dcc.Input(id={'type':'buy-strategy-2-parameter-value', 'index':1}, type='text', persistence=True)]
    }
    dictionary_sell_1 = {
        'MA': dcc.Input(id={'type':'sell-strategy-1-parameter-value', 'index':0}, type='text', persistence=True),
        'RSI': [dcc.Input(id={'type':'sell-strategy-1-parameter-value', 'index':0}, type='text', persistence=True), dcc.Input(id={'type':'sell-strategy-1-parameter-value', 'index':1}, type='text', persistence=True)]
    }
    dictionary_sell_2 = {
        'MA': dcc.Input(id={'type':'sell-strategy-2-parameter-value', 'index':0}, type='text', persistence=True),
        'RSI': [dcc.Input(id={'type':'sell-strategy-2-parameter-value', 'index':0}, type='text', persistence=True), dcc.Input(id={'type':'sell-strategy-2-parameter-value', 'index':1}, type='text', persistence=True)]
    }

    buy_strategy_1_parameter = dictionary_buy_1[buy_strategy_1_value]
    buy_strategy_2_parameter = dictionary_buy_2[buy_strategy_2_value]
    sell_strategy_1_parameter = dictionary_sell_1[sell_strategy_1_value]
    sell_strategy_2_parameter = dictionary_sell_2[sell_strategy_2_value]

    return [buy_strategy_1_parameter, buy_strategy_2_parameter, sell_strategy_1_parameter, sell_strategy_2_parameter]


@app.callback(
    Output('input-log', 'children'),
    [Input('submit-val', 'n_clicks'),],
    [
        State({'type': 'buy-strategy-1-parameter-value', 'index': ALL}, 'value'),
        State({'type': 'buy-strategy-2-parameter-value', 'index': ALL}, 'value'),
        State({'type': 'sell-strategy-1-parameter-value', 'index': ALL}, 'value'),
        State({'type': 'sell-strategy-2-parameter-value', 'index': ALL}, 'value'),
    ],
)
def display_choices(n_clicks, buy_strategy_1_parameter_value, buy_strategy_2_parameter_value, sell_strategy_1_parameter_value, sell_strategy_2_parameter_value):
    print(buy_strategy_1_parameter_value, buy_strategy_2_parameter_value, sell_strategy_1_parameter_value, sell_strategy_2_parameter_value)
    log = str(buy_strategy_1_parameter_value) + str(buy_strategy_2_parameter_value) + str(sell_strategy_1_parameter_value) + str(sell_strategy_2_parameter_value)
    return log