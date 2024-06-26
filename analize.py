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
        try:
            with open(cdir + conffile, 'r' ) as f:
                conf = eval(f.read())
                ticker_name = conf['ticker_name']
                del conf['ticker_name']
                config[ticker_name] = conf
        except:
            print(f'Error read config {conffile}')
    return config

def get_all_ticker_candles(ticker, tfs):
    candles = {}
    for tf in tfs:
        candles[tf] = db.get_all_candles(ticker, tf)
    return candles


def get_modules_chain(conf):
    chain = []

    if type(conf) == str:
        strat_path = strategies_dir + conf + '.json'
        with open(strat_path, 'r') as f:
            default_conf = eval(f.read())
    else:
        strat_path = strategies_dir + conf['base'] + '.json'
        with open(strat_path, 'r') as f:
            default_conf = eval(f.read())

        for module in default_conf['modules_conf']:
            for key in default_conf['modules_conf'][module]:
                if module in conf['modules_conf']:
                    if key in conf['modules_conf'][module]:
                        default_conf['modules_conf'][module][key] = \
                                conf['modules_conf'][module][key]
    conf = default_conf

    for mod in conf['modules_order']:
        chain.append(modules[mod](conf['modules_conf'][mod]))

    return chain

def save_solution(trade_solution, ticker, strategy):
    if ticker not in trade_solutions:
        trade_solutions[ticker] = {}
    if strategy not in trade_solutions[ticker]:
        trade_solutions[ticker][strategy] = []
    trade_solutions[ticker][strategy].append(trade_solution)

strategies_dir = './strategies/'
modules = load_modules('./modules/')
db = CandleStorage('185.58.191.251', 9000)
conf = load_configs('./configs/')
tickers = conf.keys()
trade_solutions = {}

for tik in tickers:
    tc = conf[tik]
    candles = get_all_ticker_candles(tik, tc['required_timeframes']) 

    custom_strategies = tc['trade_strategies']['custom']
    default_strategies = tc['trade_strategies']['default']

    for ds in default_strategies:
        modules_chain = get_modules_chain(ds)

        for module in modules_chain:
            solution, candles  = module.decide(candles)
            save_solution(solution, tik, ds)

    for cs in custom_strategies:
        modules_chain = get_modules_chain(cs)

        for module in modules_chain:
            solution, candles  = module.decide(candles)
            save_solution(solution, tik, cs['base'])

print(json.dumps(trade_solutions, indent=4))
