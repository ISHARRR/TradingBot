from datetime import datetime
from email.message import EmailMessage
from strats import (
    crossover,
    sma_crossover,
    basic,
    adx_ema,
    adx_ema,
    adx_test,
    adx_ema_sl,
    ema_adx_wait,
    fxstreet,
)


from datetime import date


import pytz
import recipients
import smtplib
import os
import traceback
import time
import random
import schedule


def timezone(zone):
    z = pytz.timezone(zone)
    dt = datetime.now(z).strftime("%Y-%m-%d %H:%M:%S")

    return dt


def email(buyorsell, stock_symbol, context, privacy='public'):
    msg = EmailMessage()
    msg['Subject'] = buyorsell + ': ' + stock_symbol
    msg['From'] = 'isharreehal8@gmail.com'
    if privacy == 'public':
        msg['To'] = ", ".join(recipients.recipients())
    elif privacy == 'private':
        msg['To'] = ", ".join(recipients.recipients_test())
    msg.set_content(context)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('isharreehal8@gmail.com', 'znftewujyvxesikm')

        smtp.send_message(msg)


def exception_alert(e):
    ny_time = timezone('America/New_york')
    uk_time = timezone('Europe/London')
    time_msg = 'NY-Time:' + '(' + ny_time + ') ' + \
        '| UK-Time:' + '(' + uk_time + ')'
    window_len = os.popen('stty size', 'r').read().split()
    print(' EXCEPTION ERROR '.center(int(window_len[1]), '*'))
    print('EXCEPTION ERROR', time_msg + '\n' + str(e) + '\n')
    # print ('EXCEPTION ERROR', time_msg + '\n' + str(traceback.format_exc()) + '\n' + str(e) + '\n')
    print(' EXCEPTION ERROR '.center(int(window_len[1]), '*') + '\n')


def running_msg(stock_symbol):
    ny_time = timezone('America/New_york')
    uk_time = timezone('Europe/London')
    time_msg = 'NY-Time:' + '(' + ny_time + ') ' + \
        '| UK-Time:' + '(' + uk_time + ')'
    print(stock_symbol, 'Running...', time_msg)


def trade_msg(stock_symbol, buyorsell):
    ny_time = timezone('America/New_york')
    uk_time = timezone('Europe/London')
    time_msg = '- ' + 'NY-Time:' + \
        '(' + ny_time + ') ' + '| UK-Time:' + '(' + uk_time + ')'
    print(buyorsell + ':', stock_symbol, time_msg)


def order_params(param):
    if param == 'CROSS':
        return True
    elif param == 'SL':
        return True
    elif param == 'TS':
        return True
    elif param == 'TPTS':
        return True
    else:
        return False


def exception(e):
    freq_error = "Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency."

    if str(e) == "Expecting value: line 1 column 1 (char 0)":
        pass
    elif str(e) == "('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))":
        pass
    elif str(e) == freq_error:
        pass
    else:
        exception_alert(e)
        email('TEST BOT: EXCEPTION', 'ERROR', (str(traceback.format_exc()) + '\n' + str(e)), 'private')
        time.sleep(random.randint(60, 150))

# def exception(e):
#     freq_error = "Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute and 500 calls per day. Please visit https://www.alphavantage.co/premium/ if you would like to target a higher API call frequency."
#
#     if str(e) == "Expecting value: line 1 column 1 (char 0)":
#         pass
#     elif str(e) == "('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))":
#         pass
#     elif str(e) == freq_error:
#         count = count + 1
#         mail = email('API Frequency', 'Error', freq_error + '\n' + 'Error occured ' + str(count) + ' times', 'private')
#         schedule.every().Friday.at("24:00").do(mail)
#         schedule.every().Friday.at("00:05").do()
#     else:
#         exception_alert(e)
#         email('TEST BOT: EXCEPTION', 'ERROR', (str(traceback.format_exc()) + '\n' + str(e)), 'private')
#         time.sleep(random.randint(60, 150))


def trade_ids(id, direction):
    buy_id = 0
    sell_id = 0

    if direction == 'LONG':
        buy_id = id
    elif direction == 'SHORT':
        sell_id = id

    return buy_id, sell_id


# active bots


def basic_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    basic.basic_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol)


def fxstreet_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    fxstreet.adx_ema_sl_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol)


def crossover_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    crossover.crossover_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol)


def sma_crossover_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    sma_crossover.sma_crossover_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol)


def adx_crossover_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    adx_ema.adx_crossover_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol)


def adx_crossover_ts_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    adx_ts.adx_crossover_ts_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol)


def adx_test_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    adx_test.adx_test_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol)


def adx_ema_sl_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    adx_ema_sl.adx_ema_sl_bot(stock_symbol, one_pip, api_key, oanda_stock_symbol)


def test(stock_symbol, one_pip, api_key, oanda_stock_symbol):
    ema_adx_wait.test(stock_symbol, one_pip, api_key, oanda_stock_symbol)
