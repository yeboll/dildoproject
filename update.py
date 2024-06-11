from platforms import *
from storages import CandleStorage
import argparse

platforms = {'bybit' : Bybit()}

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--ticker',  help='Тикер', required=True)
parser.add_argument('-tf', '--timeframe', help='Таймфрейм', required=True)
parser.add_argument('-p', '--platform', help='Платформа', required=True)
parser.add_argument('-a', '--addr-redis', 
                    help='Адрес Redis БД в формате ip:port', required=True)
args = parser.parse_args()

pl = platforms[args.platform]
ip, port = args.addr_redis.split(':')

db = CandleStorage(ip, port)

ld = db.get_last_candle_date(args.ticker, args.timeframe)
data = pl.get_last_candles(args.ticker, args.timeframe, ld)

for cnd in data:
    db.save_candle(args.ticker, args.timeframe, cnd)


