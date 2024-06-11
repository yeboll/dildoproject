import redis
import json

class CandleStorage:
    def __init__(self, host, port):
        self.r = redis.Redis(host=host, port=port, db=0)
        self.tf = ['M1', 'M5', 'M15', 'M30']
        self.max_size = 500

    def save_candle(self, ticker, timeframe, candle):
        key = f"{ticker}:{timeframe}"
        candle_data = {
            'Date': candle['Date'],
            'Open': candle['Open'],
            'High': candle['High'],
            'Low': candle['Low'],
            'Close': candle['Close'],
            'Volume': candle['Volume']
        }
        candle_json = json.dumps(candle_data)

        all_candles = self.get_all_candles(ticker, timeframe)
        for i, existing_candle in enumerate(all_candles):
            if existing_candle['Date'] == candle['Date']:
                self.r.lset(key, i, candle_json)
                return

        self.r.rpush(key, candle_json)
        if self.r.llen(key) > self.max_size:
            self.r.lpop(key)

    def get_all_candles(self, ticker, timeframe):
        key = f"{ticker}:{timeframe}"
        all_candles = self.r.lrange(key, 0, -1)
        candles = []
        for candle_json in all_candles:
            candle_data = json.loads(candle_json)
            candles.append(candle_data)
        return candles

    def get_last_candle_date(self, ticker, timeframe):
        key = f"{ticker}:{timeframe}"
        all_candles = self.r.lrange(key, -1, -1)
        if all_candles:
            last_candle = json.loads(all_candles[0])
            return last_candle['Date']
        else:
            return 0

