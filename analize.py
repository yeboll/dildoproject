from storages import CandleStorage

tickers = ['1000PEPEPERP', 'BTCUSDT']
tfs = ["M1", "M5", "M30", "H1", "H4", "D"]
ip, port = ('38.180.68.156', 9000)
ticker_cfg = {
    '1000PEPEPERP' : {
        'use_tfs' : ['H1'],
        'trade_strategies' : {
            'default' : ['RSI'],
            'custom' : [
                {
                    'base' : 'RSI',
					'modules_conf' : {
						'RSI' : {
							'use_tf' : ['H4']
						}
					}
                }
            ]
        }
     },

    'BTCUSDT' : {
        'use_tfs' : ['H1'],
        'trade_strategies' : {
            'default' : ['RSI'],
            'custom' : [
                {
                    'base' : 'RSI',
					'modules_conf' : {
						'RSI' : {
							'use_tf' : ['H4']
						}
					}
                }
            ]
        }
     },
}

db = CandleStorage(ip, port)

def get_all_ticker_candles(ticker, tfs):
    candles = {}
    for tf in tfs:
        candles[tf] = db.get_all_candles(ticker, tf)
    return candles

conf = {
    'Pathes' : {
        'Strategies' : './strategies/'
    }
}

def load_strategy(strat):
    strat_path = conf['Pathes']['Strategies'] 
    full_path = strat_path + strat + '/'
    return None


for tick in tickers:
    tick_conf = ticker_cfg[tick]
    # получили требуемые для анализа свечки
    big_dic = get_all_ticker_candles(tick, tick_conf['use_tfs'])
    for c in big_dic['H1']:
        print(c)

    # загружаем стандартные стратегии (которые по умолчанию)
    # анализируем свечки тикера ими каждой из стратегий
    for default in tick_conf['trade_strategies']['default']:
        strategy = load_strategy(default)









