import talib
import dash_core_components as dcc
import dash_html_components as html

# excluding SMA, MAVP, ADXR, AROON, 
dropdown_options = [
    {'label': 'Price', 'value': 'PRICE', 'type': 'overlap'},
    {'label': 'Overlap Studies: Bollinger Bands (Upper)', 'value': 'BBANDS_Up', 'type': 'overlap'},
    {'label': 'Overlap Studies: Bollinger Bands (Middle)', 'value': 'BBANDS_Mid', 'type': 'overlap'},
    {'label': 'Overlap Studies: Bollinger Bands (Lower)', 'value': 'BBANDS_Low', 'type': 'overlap'},
    {'label': 'Overlap Studies: Double Exponential Moving Average', 'value': 'DEMA', 'type': 'overlap'},
    {'label': 'Overlap Studies: Exponential Moving Average', 'value': 'EMA', 'type': 'overlap'},
    {'label': 'Overlap Studies: Hilbert Transform - Instantaneous Trendline', 'value': 'HT_TRENDLINE', 'type': 'overlap'},
    {'label': 'Overlap Studies: Kaufman Adaptive Moving Average', 'value': 'KAMA', 'type': 'overlap'},
    {'label': 'Overlap Studies: Moving average', 'value': 'MA', 'type': 'overlap'},
    {'label': 'Overlap Studies: MESA Adaptive Moving Average', 'value': 'MAMA', 'type': 'overlap'},
    {'label': 'Overlap Studies: MidPoint over period', 'value': 'MIDPOINT', 'type': 'overlap'},
    {'label': 'Overlap Studies: MidPoint Price over period', 'value': 'MIDPRICE', 'type': 'overlap'},
    {'label': 'Overlap Studies: Parabolic SAR', 'value': 'SAR', 'type': 'overlap'},
    {'label': 'Overlap Studies: Parabolic SAR - Extended', 'value': 'SAREXT', 'type': 'overlap'},
    {'label': 'Overlap Studies: Triple Exponential Moving Average (T3)', 'value': 'T3', 'type': 'overlap'},
    {'label': 'Overlap Studies: Triple Exponential Moving Average', 'value': 'TEMA', 'type': 'overlap'},
    {'label': 'Overlap Studies: Triangular Moving Average', 'value': 'TRIMA', 'type': 'overlap'},
    {'label': 'Overlap Studies: Weighted Moving Average', 'value': 'WMA', 'type': 'overlap'},
    # {'label': 'Momentum: Average Directional Movement Index', 'value': 'ADX', 'type': 'momentum'},
    # {'label': 'Momentum: Absolute Price Oscillator', 'value': 'APO', 'type': 'momentum'},
    # {'label': 'Momentum: Aroon Oscillator', 'value': 'AROONOSC', 'type': 'momentum'},
    # {'label': 'Momentum: Balance Of Power', 'value': 'BOP', 'type': 'momentum'},
]

number_of_parameters = {
    'PRICE': 0,
    'BBANDS_Up': 3,
    'BBANDS_Mid': 3,
    'BBANDS_Low': 3,
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


def create_input(strategy, direction, position):
    """
    This is the function that handle the dynamic input sequence
    """
    persistence = True
    persistence_type = 'Memory'
    input_box_style = {'font-size': '15px'}

    dictionary = {
        'PRICE': [],
        'BBANDS_Up': [
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Standard Deviation - Upper Band', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Standard Deviation - Lower Band', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
        ],
        'BBANDS_Mid': [
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Standard Deviation - Upper Band', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Standard Deviation - Lower Band', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
        ],
        'BBANDS_Low': [
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Standard Deviation - Upper Band', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Standard Deviation - Lower Band', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
        ],
        'DEMA': dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
        'EMA': dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
        'HT_TRENDLINE': [],
        'KAMA': dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
        'MA': dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
        'MAMA': [
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Fast Limit', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Slow Limit', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
        ],
        'MIDPOINT': dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
        'MIDPRICE': dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
        'SAR': [
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Acceleration', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Maximum', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
        ],
        'SAREXT': [
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Start Value', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Offset on Reverse', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Acceleration Init Long', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Acceleration Long', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Acceleration Max Long', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Acceleration Init Short', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Acceleration Short', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Acceleration Max Short', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
        ],
        'T3': [
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
            dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='V Factor', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
        ],
        'TEMA': dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
        'TRIMA': dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
        'WMA': dcc.Input(id={'type':f'{direction}-strategy-{position}-parameter-value', 'index':0}, type='number', placeholder='Time Period', persistence=persistence, persistence_type = persistence_type, style=input_box_style),
    }

    return dictionary[strategy]


def compute_technical_indicators(df, strategy_1, strategy_1_parameter, strategy_2, strategy_2_parameter):
    """
    Return the actual technical indicators that user specified
    """
    indicator = [0 ,0]

    # 
    strategy_1_parameter = [int(i) for i in strategy_1_parameter]
    strategy_2_parameter = [int(i) for i in strategy_2_parameter]

    strategy_parameters = [strategy_1_parameter, strategy_2_parameter]


    for i, strategy in enumerate([strategy_1, strategy_2]):
        if strategy == 'PRICE':
            indicator[i] = df['Close']

        elif strategy == 'BBANDS_Up':
            upperband, middleband, lowerband = talib.BBANDS(df['Close'], timeperiod=strategy_parameters[i][0], nbdevup=strategy_parameters[i][1], nbdevdn=strategy_parameters[i][2], matype=0)
            indicator[i] = upperband

        elif strategy == 'BBANDS_Mid':
            upperband, middleband, lowerband = talib.BBANDS(df['Close'], timeperiod=strategy_parameters[i][0], nbdevup=strategy_parameters[i][1], nbdevdn=strategy_parameters[i][2], matype=0)
            indicator[i] = middleband

        elif strategy == 'BBANDS_Low':
            upperband, middleband, lowerband = talib.BBANDS(df['Close'], timeperiod=strategy_parameters[i][0], nbdevup=strategy_parameters[i][1], nbdevdn=strategy_parameters[i][2], matype=0)
            indicator[i] = lowerband

        elif strategy == 'DEMA':
            indicator[i] = talib.DEMA(df['Close'], timeperiod=strategy_parameters[i][0])

        elif strategy == 'EMA':
            indicator[i] = talib.EMA(df['Close'], timeperiod=strategy_parameters[i][0])

        elif strategy == 'HT_TRENDLINE':
            indicator[i] = talib.HT_TRENDLINE(df['Close'])

        elif strategy == 'KAMA':
            indicator[i] = talib.KAMA(df['Close'], timeperiod=strategy_parameters[i][0])

        elif strategy == 'MA':
            indicator[i] = talib.MA(df['Close'], timeperiod=strategy_parameters[i][0], matype=0)

        elif strategy == 'MAMA':
            indicator[i] = talib.MAMA(df['Close'], fastlimit=strategy_parameters[i][0], slowlimit=strategy_parameters[i][1])

        elif strategy == 'MIDPOINT':
            indicator[i] = talib.MIDPOINT(df['Close'], timeperiod=strategy_parameters[i][0])

        elif strategy == 'MIDPRICE':
            indicator[i] = talib.MIDPRICE(df['High'], df['Low'], timeperiod=strategy_parameters[i][0])

        elif strategy == 'SAR':
            indicator[i] = talib.SAR(df['High'], df['Low'], acceleration=strategy_parameters[i][0], maximum=strategy_parameters[i][1])

        elif strategy == 'SAREXT':
            indicator[i] = talib.SAREXT(df['High'], df['Low'], startvalue=strategy_parameters[i][0], offsetonreverse=strategy_parameters[i][1], 
                                        accelerationinitlong=strategy_parameters[i][2], accelerationlong=strategy_parameters[i][3], 
                                        accelerationmaxlong=strategy_parameters[i][4], accelerationinitshort=strategy_parameters[i][5], 
                                        accelerationshort=strategy_parameters[i][6], accelerationmaxshort=strategy_parameters[i][7])

        elif strategy == 'T3':
            indicator[i] = talib.T3(df['Close'], timeperiod=strategy_parameters[i][0], vfactor=strategy_parameters[i][1])

        elif strategy == 'TEMA':
            indicator[i] = talib.TEMA(df['Close'], timeperiod=strategy_parameters[i][0])

        elif strategy == 'TRIMA':
            indicator[i] = talib.TRIMA(df['Close'], timeperiod=strategy_parameters[i][0])

        elif strategy == 'WMA':
            indicator[i] = talib.WMA(df['Close'], timeperiod=strategy_parameters[i][0])

    return (indicator[0], indicator[1])
