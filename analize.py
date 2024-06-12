from storages import CandleStorage
from importlib import import_module
import pandas as pd
import os, json

def load_modules(mdir):
    modules = {}
    for modulefile in os.listdir(mdir):
        try:
            module_name = mdir.replace('./', '') + \
                    modulefile.replace('.py', '') 
            module_name = module_name.replace('/', '.')
            class_name = modulefile.replace('.py', '') 

            module = import_module(module_name)
            modules[class_name] = getattr(module, class_name)
        except:
            print(f'Error import module {module_name}') 

    return modules

def load_configs(cdir):
    config = {}
    for conffile in os.listdir(cdir):
        with open(cdir + conffile, 'r' ) as f:
            conf = eval(f.read())
            ticker_name = conf['ticker_name']
            del conf['ticker_name']
            config[ticker_name] = conf
    return config

def get_all_ticker_candles(ticker, tfs):
    candles = {}
    for tf in tfs:
        candles[tf] = db.get_all_candles(ticker, tf)
    return candles


def get_modules_chain(conf):
    chain = []

    if conf['type'] == 'default':
        strat_path = strategies_dir + conf['path']
        with open(strat_path, 'r') as f:
            conf = eval(f.read())

    for module in conf['modules_order']:
        if module not in modules:
            continue
        chain.append(modules[module](conf['modules_conf'][module]))

    return chain

def save_solution(trade_solution, ticker, strategy):
    if ticker not in trade_solutions:
        trade_solutions[ticker] = {}
    if strategy not in trade_solutions[ticker]:
        trade_solutions[ticker][strategy] = {}
    trade_solutions[ticker][strategy] = trade_solution

strategies_dir = './strategies/'
modules = load_modules('./modules/')
db = CandleStorage('185.58.191.251', 9000)
conf = load_configs('./configs/')
tickers = conf.keys()
trade_solutions = {}

for tik in tickers:
    tc = conf[tik]
    candles = get_all_ticker_candles(tik, tc['required_timeframes']) 

    for strategy in tc['trade_strategies']:
        modules_chain = get_modules_chain(tc['trade_strategies'][strategy])
        for module in modules_chain:
            solution, candles  = module.decide(candles)
            save_solution(solution, tik, strategy)

print(json.dumps(trade_solutions, indent=4))
