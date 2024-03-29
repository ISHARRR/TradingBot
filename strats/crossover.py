
from indicators import (
    ema_sma,

)
from trades_database import db


import bot
import oanda
import time
import random
import traceback


def crossover_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    bot.running_msg(stock_symbol)

    account = '101-004-14591208-007'

    cross = oanda.Oanda(account, oanda_stock_symbol, one_pip, 0.95, 'FAKE')
    database = 'trades_database/crossDB'

    id, direction = cross.get_open_trade()
    db.createDB(database, id, direction)

    buy_id = db.getDB('BUY', databacse)
    sell_id = db.getDB('SELL', database)

    fast_ema = 20
    slow_ema = 50

    while True:
        try:
            current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.double_ema(
                stock_symbol, api_key, fast_ema, slow_ema)

            email_message = 'Crossover Strategy'

            if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow)):  # BUY
                bot.trade_msg(stock_symbol, 'BUY')
                # email('BUY', stock_symbol, email_message)
                bot.email('BUY - test', stock_symbol, email_message, 'private')
                if sell_id != 0:
                    cross.close_order(sell_id)
                    print('Trade ID:', sell_id, 'Status: CLOSED' + '\n')
                    bot.email('Order Closed - test', str(sell_id),
                              'Check if order has been closed', 'private')

                    sell_id = db.updateDB('SELL', 0, database)

                if cross.get_open_trade_count() < 1:
                    trade_id = cross.create_order('CROSS', 'BUY')
                    buy_id = db.updateDB('BUY', trade_id, database)

                while True:
                    time.sleep(60)
                    try:
                        current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.double_ema(
                            stock_symbol, api_key, fast_ema, slow_ema)

                        if ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow)):  # SELL
                            if buy_id != 0:
                                cross.close_order(buy_id)
                                print('Trade ID:', buy_id,
                                      'Status: CLOSED' + '\n')
                                bot.email('Order Closed - test', str(buy_id),
                                          'Check if order has been closed', 'private')
                                buy_id = db.updateDB('BUY', 0, database)

                            bot.trade_msg(stock_symbol, 'SELL')
                            # email('SELL', stock_symbol, email_message)
                            bot.email('SELL - test', stock_symbol,
                                      email_message, 'private')

                            if cross.get_open_trade_count() < 1:
                                trade_id = cross.create_order('CROSS', 'SELL')
                                sell_id = db.updateDB('SELL', trade_id, database)

                            break

                    except Exception as e:
                        bot.exception_alert(e)
                        bot.email('TEST BOT: EXCEPTION ERROR -', 'INNER LOOP',(str(traceback.format_exc()) + '\n' + str(e)), 'private')
                        time.sleep(random.randint(60, 150))

                    time.sleep(240)

            if ((current_ema_fast < current_ema_slow) and (previous_ema_fast >= previous_ema_slow)):  # SELL
                bot.trade_msg(stock_symbol, 'SELL')
                # email('SELL', stock_symbol, email_message)
                bot.email('SELL - test', stock_symbol,
                          email_message, 'private')
                if buy_id != 0:
                    cross.close_order(buy_id)
                    print('Trade ID:', buy_id, 'Status: CLOSED' + '\n')
                    bot.email('Order Closed - test', str(buy_id),
                              'Check if order has been closed', 'private')
                    buy_id = db.updateDB('BUY', 0, database)

                if cross.get_open_trade_count() < 1:
                    trade_id = cross.create_order('CROSS', 'SELL')
                    sell_id = db.updateDB('SELL', trade_id, database)

                while True:
                    time.sleep(60)
                    try:
                        current_ema_fast, current_ema_slow, previous_ema_fast, previous_ema_slow = ema_sma.double_ema(
                            stock_symbol, api_key, fast_ema, slow_ema)

                        if ((current_ema_fast > current_ema_slow) and (previous_ema_fast <= previous_ema_slow)):  # BUY
                            if sell_id != 0:
                                cross.close_order(sell_id)
                                print('Trade ID:', sell_id,
                                      'Status: CLOSED' + '\n')
                                bot.email('Order Closed - test', str(sell_id),
                                          'Check if order has been closed', 'private')
                                sell_id = db.updateDB('SELL', 0, database)

                            bot.trade_msg(stock_symbol, 'BUY')
                            # email('BUY', stock_symbol, email_message)
                            bot.email('BUY - test', stock_symbol,
                                      email_message, 'private')

                            if cross.get_open_trade_count() < 1:
                                trade_id = cross.create_order('CROSS', 'BUY')
                                buy_id = db.updateDB('BUY', trade_id, database)

                            break

                    except Exception as e:
                        bot.exception_alert(e)
                        bot.email('TEST BOT: EXCEPTION ERROR -', 'INNER LOOP',(str(traceback.format_exc()) + '\n' + str(e)), 'private')
                        time.sleep(random.randint(60, 150))

                    time.sleep(240)

        except Exception as e:
            bot.exception_alert(e)
            bot.email('TEST BOT: EXCEPTION', 'ERROR',(str(traceback.format_exc()) + '\n' + str(e)), 'private')
            time.sleep(random.randint(60, 150))

        time.sleep(300)
