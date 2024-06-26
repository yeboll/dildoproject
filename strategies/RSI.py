from base import Strategy

class RSI(Strategy):

    def decide(self, data):

        mod = self.modules[0]
        module_name = mod['name']
        module_obj = mod['obj']

        data = module_obj.analize(data)
        result = data[self.conf[module_name]['use_tf'][0]]
        rsi = result[-1]['RSI']
        
        if rsi < 30:
            self.sol['action'] = 'buy'
        elif rsi > 70:
            self.sol['action'] = 'sell'
        else: self.sol['action'] = 'keep'

        return (self.sol, data)
