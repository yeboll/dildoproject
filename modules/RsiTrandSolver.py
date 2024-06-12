import pandas as pd
import ta
import pandas_ta as ta
from module import Module

class RsiTrandSolver(Module):

    def is_trand_up(self, line_avg):
        return line_avg[0] > line_avg[len(line_avg)-1]


    def decide(self, data):
        low_tf_candles = pd.DataFrame(data[self.conf['low_tf']])
        high_tf_candles = pd.DataFrame(data[self.conf['high_tf']])

        # если тренд старшего таймфрейма ебашит 
        # вверх то 100 проц ищем сделки на покупку
        # на младшем таймфрейме, при условии, что
        # тренд на младшем ебашит вниз и низкий rsi
        if self.is_trand_up(high_tf_candles['AVG']):
            if not self.is_trand_up(low_tf_candles['AVG']):
                if low_tf_candles['RSI'][len(low_tf_candles) -1] <= 30:
                    self.sol['action'] = 'buy'

        # если ебашит вниз, то все наоборот
        elif not self.is_trand_up(high_tf_candles['AVG']):
            if  self.is_trand_up(low_tf_candles['AVG']):
                if low_tf_candles['RSI'][len(low_tf_candles) - 1] >= 70:
                    self.sol['action'] = 'sell'
        
        # если не туда не туда - нахуй надo
        if self.sol['action'] == None:
            self.sol['action'] = 'keep'

        return (self.sol, data)


