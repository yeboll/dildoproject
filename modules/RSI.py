import pandas as pd
import ta
import pandas_ta as ta

class RSI():

    def __init__(self, conf):
        self.conf = conf
        self.models = {}

    def decide(self, data):
        use_tf = self.conf['use_tf']
        len_ = self.conf['len']
        
        for tf in use_tf:
            df = pd.DataFrame(data[tf])
            df['RSI'] = ta.momentum.rsi(df['Close'], window=len_)
            res = df.to_dict('records')
            data[tf] = res
            
        return (None, data)
        


