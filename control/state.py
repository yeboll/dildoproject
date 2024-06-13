import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from platforms import Bybit
from cron import is_cron_job_exists


class State():

    states = {}
    available_tfs = ['M1', 'M5', 'M15',  'M30', 'H1', 'H4', 'D', 'W', 'M']
    available_strategies = ['RSI', 'SmartMonye']

    def __init__(self):
        for t in Bybit().get_avaliable_tikers():
            self.states[t] = {
                'recv_tf' : [],
                'strategies' : []
            }
            for tf in self.available_tfs:
                if is_cron_job_exists(t, tf):
                    self.states[t]['recv_tf'].append(tf)



