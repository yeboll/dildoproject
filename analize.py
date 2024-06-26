from storages import CandleStorage
from importlib import import_module
import os

pathes = {
    'tickers_configs' : 'configs/tickers/',
    'default_strategies_configs' : 'configs/strategies/',
    'strategies' : 'strategies/',
    'modules' : 'modules/'
}

def load_conf(file):
    with open(file, 'r')  as f:
        return eval(f.read())

def get_all_ticker_candles(ticker, tfs):
    candles = {}
    for tf in tfs:
        candles[tf] = db.get_all_candles(ticker, tf)
    return candles

def load_strategy(strat):
    strat_dir = pathes['strategies']
    strat_conf_dir = pathes['default_strategies_configs']
    strat_cfg = load_conf(strat_conf_dir + strat + '.json')
    mod = strat_dir.replace('/', '.') + strat
    module = import_module(mod)
    class_ = getattr(module, strat)
    return class_(strat_cfg)

def load_tickers_configs():
    path = pathes['tickers_configs']
    confs = {}
    for filename in os.listdir(path):
        ticker_name = filename.replace('.json', '')
        confs[ticker_name] = load_conf(path + filename)
    return confs

db = CandleStorage('38.180.68.156', 9000)
conf = load_tickers_configs()

for tick in conf.keys():
    tick_conf = conf[tick]

    # получили требуемые для анализа свечки
    big_dic = get_all_ticker_candles(tick, tick_conf['required_timeframes'])

    # загружаем стандартные стратегии (которые по умолчанию)
    # анализируем свечки тикера каждой из стратегий
    for default in tick_conf['trade_strategies']['default']:
        strategy = load_strategy(default)
        print(default, tick, strategy.decide(big_dic)[0])


