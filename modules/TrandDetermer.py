import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from module import Module

class TrandDetermer(Module):

    def trand_determ(self, df):
        df_cp = pd.DataFrame(df)
        X = np.arange(len(df_cp)).reshape(-1, 1)
        y = df_cp['Close'].values
        model = LinearRegression()
        model.fit(X, y)

        df_cp['AVG'] = model.predict(X)
        return df_cp.to_dict('records')

    def decide(self, data):
        hkey = self.conf['tf_high']
        lkey = self.conf['tf_low']

        high_tf_candles = data[hkey]
        low_tf_candles = data[lkey]

        high_tf_trand = self.trand_determ(high_tf_candles)
        low_tf_trand = self.trand_determ(low_tf_candles)

        data[hkey] = high_tf_trand
        data[lkey] = low_tf_trand

        # df['DateTime'] = pd.to_datetime(df['Date'])
        # mpf.plot(df.set_index('DateTime'), type='candle', volume=True, 
        #         addplot=[mpf.make_addplot(df['AVG'], panel=0, color='red')])

        return (self.sol, data)
        


