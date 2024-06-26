import pandas as pd
import ta
import pandas_ta as ta
from base import Module

class RSI(Module):

    def analize(self, data):

        use_tf = self.conf['use_tf']
        len_ = self.conf['len']
        
        for tf in use_tf:
            df = pd.DataFrame(data[tf])
            df['RSI'] = ta.momentum.rsi(df['Close'], window=len_)
            res = df.to_dict('records')
            data[tf] = res

        return data
        
