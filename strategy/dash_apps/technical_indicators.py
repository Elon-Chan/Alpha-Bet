import talib
import dash_core_components as dcc
import dash_html_components as html

# excluding SMA and MAVP
dropdown_options = [
    {'label': 'Overlap Studies: Bollinger Bands', 'value': 'BBANDS'},
    {'label': 'Overlap Studies: Double Exponential Moving Average', 'value': 'DEMA'},
    {'label': 'Overlap Studies: Exponential Moving Average', 'value': 'EMA'},
    {'label': 'Overlap Studies: Hilbert Transform - Instantaneous Trendline', 'value': 'HT_TRENDLINE'},
    {'label': 'Overlap Studies: Kaufman Adaptive Moving Average', 'value': 'KAMA'},
    {'label': 'Overlap Studies: Moving average', 'value': 'MA'},
    {'label': 'Overlap Studies: MESA Adaptive Moving Average', 'value': 'MAMA'},
    {'label': 'Overlap Studies: MidPoint over period', 'value': 'MIDPOINT'},
    {'label': 'Overlap Studies: Parabolic SAR', 'value': 'SAR'},
    {'label': 'Overlap Studies: Parabolic SAR - Extended', 'value': 'SAREXT'},
    {'label': 'Overlap Studies: Simple Moving Average', 'value': 'SMA'},
    {'label': 'Overlap Studies: Triple Exponential Moving Average (T3)', 'value': 'T3'},
    {'label': 'Overlap Studies: Triple Exponential Moving Average', 'value': 'TEMA'},
    {'label': 'Overlap Studies: Triangular Moving Average', 'value': 'TRIMA'},
    {'label': 'Overlap Studies: Weighted Moving Average', 'value': 'WMA'},
]

number_of_parameters = {
    'BBANDS': 3,
    'DEMA': 1,
    'EMA': 1,
    'HT_TRENDLINE': 0,
    'KAMA': 1,
    'MA': 1,
    'MAMA': 2,
    'MIDPOINT': 1,
    'MIDPRICE': 1,
    'SAR': 2,
    'SAREXT': 8,
    'T3': 2,
    'TEMA': 1,
    'TRIMA': 1,
    'WMA': 1,
}

persistence = True
persistence_type = 'Memory'

dictionary_buy_1 = {
    'BBANDS': [
        dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type),
        dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Standard Deviation - Upper Band', persistence=persistence, persistence_type = persistence_type),
        dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Standard Deviation - Lower Band', persistence=persistence, persistence_type = persistence_type),
    ],
    'DEMA': dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type),
    'EMA': dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type),
    'HT_TRENDLINE': [],
    'KAMA': dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type),
    'MA': dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type),
    'MAMA': [
        dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Fast Limit', persistence=persistence, persistence_type = persistence_type),
        dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Slow Limit', persistence=persistence, persistence_type = persistence_type),
    ],
    'MIDPOINT': dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type),
    'MIDPRICE': dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type),
    'SAR': [
        dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Acceleration', persistence=persistence, persistence_type = persistence_type),
        dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Maximum', persistence=persistence, persistence_type = persistence_type),
    ],
    'SAREXT': [
        dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Start Value', persistence=persistence, persistence_type = persistence_type),
        dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Offset on Reverse', persistence=persistence, persistence_type = persistence_type),
        dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Acceleration Init Long', persistence=persistence, persistence_type = persistence_type),
        dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Acceleration Long', persistence=persistence, persistence_type = persistence_type),
        dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Acceleration Max Long', persistence=persistence, persistence_type = persistence_type),
        dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Acceleration Init Short', persistence=persistence, persistence_type = persistence_type),
        dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Acceleration Short', persistence=persistence, persistence_type = persistence_type),
        dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Acceleration Max Short', persistence=persistence, persistence_type = persistence_type),
    ],
    'T3': [
        dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type),
        dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='V Factor', persistence=persistence, persistence_type = persistence_type),
    ],
    'TEMA': dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type),
    'TRIMA': dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type),
    'WMA': dcc.Input(id={'type':'buy-strategy-1-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type),
}

dictionary_buy_2 = dictionary_buy_1
dictionary_sell_1 = dictionary_buy_1
dictionary_sell_2 = dictionary_buy_1

def compute_technical_indicators(df, strategy_1, strategy_1_parameter, strategy_2, strategy_2_parameter):

    indicator = [indicator_1, indicator_2]

    for i, strategy in enumerate([strategy_1, strategy_2]):
        if strategy == 'BBANDS':
                pass
        elif strategy == 'MA':
            indicator[i] = talib.MA(df['Close'], timeperiod=int(strategy_1_parameter[0]), matype=0)


    # if strategy_1 == 'MA':
    #     indicator_1 = talib.MA(df['Close'], timeperiod=int(strategy_1_parameter[0]), matype=0)
    # elif strategy_1 == 'RSI':
    #     indicator_1 = talib.RSI(df['Close'], timeperiod=int(strategy_1_parameter[0]))

    # if strategy_2 == 'MA':
    #     indicator_2 = talib.MA(df['Close'], timeperiod=int(strategy_2_parameter[0]), matype=0)
    # elif strategy_2 == 'RSI':
    #     indicator_2 = talib.RSI(df['Close'], timeperiod=int(strategy_2_parameter[0]))

    return [indicator_1, indicator_2]
