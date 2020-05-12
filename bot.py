from datetime import datetime
from strategies import ema_sma

import time
import pytz
import random
import recipients
import oanda


def timezone(zone):
    z = pytz.timezone(zone)
    dt = datetime.now(z).strftime("%Y-%m-%d %H:%M:%S")

    return dt


def trade(stock_symbol, api_key, oanda_stock_symbol):
    ny_time = timezone('America/New_york')
    uk_time = timezone('Europe/London')
    time_msg = 'NY-Time:' + '(' + ny_time +') ' + '| UK-Time:' + '(' + uk_time +')'
    print(stock_symbol, 'Running...', time_msg )

    while True:
        ny_time = timezone('America/New_york')
        uk_time = timezone('Europe/London')

        time_msg = '- ' + 'NY-Time:' + '(' + ny_time +') ' + '| UK-Time:' + '(' + uk_time +')'

        try:
            current_sma100, current_sma200 = ema_sma.sma(stock_symbol, api_key)
            # current_sma100, current_sma200 = sma(stock_symbol, api_key)
            current_ema5, current_ema15, previous_ema5, previous_ema15 = ema_sma.ema(stock_symbol, api_key)

            if ((current_ema5 > current_ema15) and (previous_ema5 < previous_ema15) and (current_sma100 > current_sma200)): # BUY
                print('BUY:', stock_symbol, time_msg)
                email('BUY', stock_symbol)
                oanda.create_order(oanda_stock_symbol, 0.1, 'BUY')
                time.sleep(900)

            if ((current_ema5 < current_ema15) and (previous_ema5 > previous_ema15) and (current_sma100 < current_sma200)): # SELL
                print('SELL:', stock_symbol, time_msg)
                email('SELL', stock_symbol)
                oanda.create_order(oanda_stock_symbol, 0.1, 'SELL')
                time.sleep(900)

        except:
            print ('EXCEPTION ERROR', time_msg)
            time.sleep(random.randint(30, 150))

        time.sleep(600)

# sma('EURUSD', '4OKNDHHTQH2CFWZ9')
# ema('GBPUSD', 'T7NT8GKR7CJ36U3C')
