import os

conf_dir = '../configs/'

def update_ticker_strategies(tik, strat_conf):
    ...

def get_ticker_strategies_conf(tik):
    low = tik.lower()
    file = low.replace('usdt', '') + '.json'
    if os.path.exists(conf_dir + file):
        with open(conf_dir + file, 'r') as f:
            conf = eval(f.read())
            strat = conf['trade_strategies']
            return strat
    return {}
            
             
    

