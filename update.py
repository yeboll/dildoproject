from platforms import *
from storages import CandleStorage
import argparse
from time import sleep

platforms = {'bybit' : Bybit()}

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--platform', help='Платформа', required=True)
parser.add_argument('-tf', '--timeframe', help='Таймфрейм', required=True)
parser.add_argument('-a', '--addr-redis', 
                    help='Адрес Redis БД в формате ip:port', required=True)
args = parser.parse_args()

pl = platforms[args.platform]
ip, port = args.addr_redis.split(':')

db = CandleStorage(ip, port)

for ticker in pl.get_avaliable_tikers():
    ld = db.get_last_candle_date(ticker, args.timeframe)
    data = pl.get_last_candles(ticker, args.timeframe, ld)
    print(ticker, args.timeframe, len(data))
    sleep(0.05)

    for cnd in data:
        db.save_candle(ticker, args.timeframe, cnd)


