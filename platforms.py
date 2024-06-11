from abc import ABC, abstractmethod
from datetime import datetime
from pybit.unified_trading import HTTP

class Platform(ABC):
    @abstractmethod
    def get_avaliable_tikers(self) -> []:
        ...

    @abstractmethod
    def get_last_candles(self, tiker, tf, time = 0) -> []:
        ...


class Bybit(Platform):
    
    session = HTTP()

    def get_avaliable_tikers(self) -> []:
        api_url = self.session.get_tickers(category="linear")
        tickers = api_url['result']['list']
        list_info_tickers = []
        for t in tickers:
            list_info_tickers.append(t['symbol'])
        return list_info_tickers


    def tf2interval(self, tf):
        interval = 0
        if tf[0] == 'M': # минутка
            return int(tf[1:])
        elif tf[0] == 'H':  # часовик
            return int(tf[1:]) * 60
        else: return tf[0]

    def strtime2timestamp(self, strtime):
        if strtime == 0:
            return 0
        return datetime.strptime(strtime, '%Y-%m-%d %H:%M:%S').timestamp() * 1000


    def get_last_candles(self, tiker, tf, time = 0) -> []:
        response = self.session.get_kline(category="linear",
                                     symbol=tiker,
                                     interval=self.tf2interval(tf),
                                     start=self.strtime2timestamp(time),
                                     end=datetime.now().timestamp())
        candles = response['result']['list']

        data = [
            {
                'Date': datetime.fromtimestamp(int(candle[0]) / 1000).\
                        strftime('%Y-%m-%d %H:%M:%S'),
                'Open': float(candle[1]),
                'High': float(candle[2]),
                'Low': float(candle[3]),
                'Close': float(candle[4]),
                'Volume': float(candle[5])
            }
            for candle in candles
        ]

        if len(data) == 0:
            return self.get_last_candles(tiker, tf, 0)
        
        return data[::-1]
