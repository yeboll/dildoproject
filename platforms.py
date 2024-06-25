from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pybit.unified_trading import HTTP
from time import sleep

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
        if tf[0] == 'M':
            return int(tf[1:])
        elif tf[0] == 'H':
            return int(tf[1:]) * 60
        else: return tf[0]

    def tf2sec(self, tf):
        res = self.tf2interval(tf)
        if res == 'D':
            return 24 * 60 * 60
        if res == 'W':
            return 24 * 60 * 60 * 7
        if res == 'M':
            return 24 * 60 * 60 * 31
        else: return res * 60

    def strtime2timestamp(self, strtime):
        if strtime == 0:
            return 0
        return datetime.strptime(strtime, '%Y-%m-%d %H:%M:%S').timestamp() * 1000


    def get_last_candles(self, tiker, tf, time = 0) -> []:

        candles = []
        start_time = self.strtime2timestamp(time)
        max_candles_to_receive = 5000
        steps = 1

        if start_time == 0:
            cur = datetime.now()
            cur = cur - timedelta(seconds=cur.second, microseconds=cur.microsecond)
            cur = cur.timestamp()
            start_time = cur - self.tf2sec(tf) * max_candles_to_receive
            start_time = start_time * 1000
            steps = 5

        for i in range(steps):
            response = self.session.get_kline(category="linear",
                                         symbol=tiker,
                                         interval=self.tf2interval(tf),
                                         start=start_time,
                                         limit=1000)
            cnd = response['result']['list']
            start_time = int(cnd[0][0])
            for c in cnd: candles.append(c)
        
        candles.sort()
        candles = candles[::-1]

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

        return data[::-1]
