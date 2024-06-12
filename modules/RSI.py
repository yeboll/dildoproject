import pandas as pd
import ta
import pandas_ta as ta
from module import Module

class RSI(Module):

    def decide(self, data):
        use_tf = self.conf['use_tf']
        len_ = self.conf['len']
        
        for tf in use_tf:
            df = pd.DataFrame(data[tf])
            df['RSI'] = ta.momentum.rsi(df['Close'], window=len_)
            res = df.to_dict('records')
            data[tf] = res

        if len(use_tf) == 1:
            tf_df = data[use_tf[0]]
            last_rsi = tf_df[-1]['RSI']

            if last_rsi <= 30:
                self.sol['action'] = 'buy'
            elif last_rsi >= 70:
                self.sol['action'] = 'sell'
            else: 
                self.sol['action'] = 'keep'
            self.sol['log'].append(f"RSI on tf {use_tf[0]}: {last_rsi}")
            
        return (self.sol, data)
        
