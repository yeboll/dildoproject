from base import Strategy
import pandas as pd

class TrandPlusRSI(Strategy):

    def is_trand_up(self, line_avg):
        return line_avg[0] > line_avg[len(line_avg)-1]

    def decide(self, data):

        for trade_module in self.modules:
            module_name = trade_module['name']
            module_obj = trade_module['obj']
            data = module_obj.analize(data)

        try:
            low_tf_candles = pd.DataFrame(data[self.conf['TrandDetermer']['tf_low']])
            high_tf_candles = pd.DataFrame(data[self.conf['TrandDetermer']['tf_high']])

            # если тренд старшего таймфрейма ебашит
            # вверх то 100 проц ищем сделки на покупку
            # на младшем таймфрейме, при условии, что
            # тренд на младшем ебашит вниз и низкий rsi
            if self.is_trand_up(high_tf_candles['AVG']):
                if not self.is_trand_up(low_tf_candles['AVG']):
                    if high_tf_candles['RSI'][len(high_tf_candles) -1] <= 30:
                        self.sol['action'] = 'buy'

            # если ебашит вниз, то все наоборот
            elif not self.is_trand_up(high_tf_candles['AVG']):
                if  self.is_trand_up(low_tf_candles['AVG']):
                    if high_tf_candles['RSI'][len(high_tf_candles) - 1] >= 70:
                        self.sol['action'] = 'sell'

            # если не туда не туда - нахуй надo
            if self.sol['action'] == None:
                self.sol['action'] = 'keep'
        except:
            self.sol['log'] = 'error'

        return (self.sol, data)
