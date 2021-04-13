import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL
import plotly.express as px
import plotly.graph_objects as go


import pandas as pd
import yfinance as yf
# django plotly dash
from django_plotly_dash import DjangoDash

disclaim = 'The content of this webpage is not an investment advice and does not constitute any offer or solicitation to offer or recommendation of any investment product. It is for general purposes only and does not take into account your individual needs, investment objectives and specific financial circumstances. Investment involves risk. The investor type classification has no relationship with and is not any substitute for the Financial Needs Analysis (the “FNA”) or your risk profiling under the FNA. You instruct us that if there is any conflict or inconsistency between the investor type classification and your investment risk profiling under the FNA, the latter shall prevail and be used for assessing your risk profile for your conducting investment product transaction with our Bank. Please also note that asset allocation does not generate positive return or protection against market loss.'

app = DjangoDash('hedge', add_bootstrap_links=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

def blank_figure():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None,
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0),paper_bgcolor = 'rgba(0,0,0,0)',plot_bgcolor = 'rgba(0,0,0,0)')
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    
    return fig



app.layout =  html.Div([
        dbc.CardHeader([
                        html.H1("Risk Hedger",style={'text-align': 'center', 'font-family': 'HaextPlain', 'color': 'white'}),
                        html.Br(),
                        html.H3("Riskless Investment", style={'text-align': 'center', 'font-family': 'AspergitRegular', 'color': 'white'})]
        ),
        dbc.CardBody([
            dbc.Card([
                dbc.CardBody([
                        dbc.Row([
                            dbc.Col([html.Button("Add Stock", id="add-stock", n_clicks=0,
                            style={"margin-left": "-785px","margin-top": "30px", 'font-size': '16px'})]),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.Div(id='input-container', children=[]),
                            ]),
                        ]),
                ])
            ],color="secondary"),
            html.Div(
                children=[dbc.Button(
                    'Hedge', id='hedge',
                    n_clicks=0,
                    outline=True,
                    color="primary",
                    className="mr-1",
                    style={
                        "font-size": "25px",
                        'color': 'white',
                        'font-family': 'HaextPlain',
                        'font-weight': 'bold',
                        "padding-top": "10px",
                        "padding-bottom": '20px',
                        "padding-right": "40px",
                        "padding-left":"50px",
                        "border-radius": "6px",
                        "margin-top": "30px",
                        "margin-bottom": "30px"
                    }
                )],
                style={'text-align': 'center'}
            ),
            dbc.Card([
                dbc.CardBody([
                    html.Div(children=dcc.Graph(id="pie-chart", figure = blank_figure(), style={'align':'center'})),
                    html.Div(id='portfolio-beta', style={'font-size': '30px','text-align': 'center', 'font-family': 'AspergitRegular', 'color': 'white'}),
                    html.Div(id='disclaimer', children=f'Disclaimer: {disclaim}')
                ])
            ],color="secondary")
        ])
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
            style={"margin-right": '50px','font-size': '15px'}
        ),
        dcc.Input(
        id = {
                'type': 'num-shares',
                'index': n_clicks
            },
            type='number',
            style={'font-size': '15px', }
        )
    ]

    children.append(html.Br())
    children.append(html.Span(children=f'Stock {n_clicks + 1}: ', style={'font-size': '25px', 'color': 'white',}))
    children.append(new_input[0])
    children.append(html.Span(children=f'Number of Shares: ', style={'font-size': '25px', 'color': 'white'}))
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
    
    pull = [0.1] * len(df)
    largest_stock = df['Weight'].idxmax()
    pull[largest_stock] = 0.3

    fig = go.Figure(data=[go.Pie(labels=stock_tickers, values=individual_stock_weight, pull=pull, title='Your portfolio formation: ')])
    fig.update_layout(paper_bgcolor = 'rgba(0,0,0,0)',
                    plot_bgcolor = 'rgba(0,0,0,0)',
                    autosize=True,
                    font=dict(
                        size=24,
                        color='white',
                        family='AspergitRegular'
                        ))

    required_size = portfolio_size / 3 * portfolio_beta
    # get inverse instructmetns data
    SPXU = yf.Ticker('SPXU')
    SPXU_price = SPXU.history(period='1d')['Close'][0]

    required_inverse_stock = required_size/SPXU_price

    hedge_message = f'You need approximately {int(required_inverse_stock)} shares of SPXU to hedge your market risk in your portfolio.*'

    return fig, hedge_message