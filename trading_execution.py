# Imports

import os
import time
import numpy as np
import pandas as pd
from pandas.tseries.offsets import BMonthEnd
from datetime import datetime, timezone
from dotenv import load_dotenv
from alpaca_trade_api import REST, TimeFrame

TICKERS = ['SPY', 'QQQ']
lookback_time = 63 # Around 3 months worth of trading days
run_after_et_hour = 16 # I make my decision after the market has closed at 4 p.m ET

# Checker

def trading_time_ok():
    now = datetime.now()
    return now.hour >= run_after_et_hour

# Helper function

def month_end_index(dates: pd.DataFrame):
    df = pd.DataFrame(index=dates)
    months_end = df.groupby([df.index.year, df.index.month]).tail(1).index
    return months_end

# API checker

def get_api():
    load_dotenv()  # reads .env 
    base = os.getenv('ALPACA_BASE_URL', 'https://paper-api.alpaca.markets')
    key  = os.getenv('ALPACA_API_KEY_ID')
    sec  = os.getenv('ALPACA_API_SECRET_KEY')

    # Safety checks
    if not key or not sec:
        print('Missing API keys. Put them in an .env file as ALPACA_API_KEY_ID and ALPACA_API_SECRET_KEY.')
    return REST(key_id=key, secret_key=sec, base_url=base)

# Get daily close prices from API

def daily_close_prices(api: REST, symbols: list[str], start: str, end: None):
    frames = []
    for sym in symbols:
        bars = api.get_bars(sym, TimeFrame.Day, start, end, limit=5000).df
        if bars.empty:
            raise ValueError(f'No bars found for {sym}')
        s = bars['close']
        s.name = sym
        frames.append(s)
        time.sleep(0.25)
    prices = pd.concat(frames, axis=1).sort_index()
    prices.index = pd.to_datetime(prices.index).tz_localize(None) # We want there to be no timezone bias

    return prices


def monthly_choice(prices: pd.DataFrame):
    momentum = prices.pct_change(lookback_time)
    
    months_end = month_end_index(momentum.index)
    signals = momentum.reindex(months_end).copy()

    choice_decision = np.where(signals['SPY'] > signals['QQQ'], 'SPY', 'QQQ')
    choice_series = pd.Series(choice_decision, index=signals.index, name='choice')
    
    choice = choice_series.shift(1)
    return choice 


# Trade logic

def get_current_positions(api: REST):
    positions = api.list_positions()
    for pos in positions:
        if pos.symbol in TICKERS:
            return pos.symbol
    return 

def trading_our_choice(api, target_symbol, target_notional):
    current = get_current_positions(get_api())

    if current == target_symbol:
        print(f'Do nothing. We are already holding our choice: {target_symbol}')
    
    elif current == None:
        print(f'Had no positions. Now buying {target_symbol}')

        api.submit_order(
            symbol=target_symbol,
            side='buy',
            type='market',
            notional=target_notional,
            time_in_force='day'
        )
    else:
        api.submit_order(
            symbol=current,
            side='sell',
            type='market',
            qty=api.get_position(current).qty,
            time_in_force='day'
        )

        api.submit_order(
            symbol=target_symbol,
            side='buy',
            type='market',
            notional=target_notional,
            time_in_force='day'
        )


# Main

if __name__ == '__main__':
    if trading_time_ok():
    # Checking to see if today is last trading day of the month.
        today = pd.Timestamp.today().normalize()
    
        if today == today + BMonthEnd(0): # BMonthEnd 
            print('Today is the last trading day of the month. Running strategy.')
       
            prices = daily_close_prices(get_api(), TICKERS, start = '2024-01-01', end = None)
            choice = monthly_choice(prices) 

    # Takes our latest decision that falls on the end of the month

            valid_dates = choice.index[choice.index <= today]
            if not valid_dates.empty:
                most_recent_valid_decision = valid_dates[-1]
                target_etf = choice.loc[most_recent_valid_decision]

                print(f'Signal says to hold {target_etf}.')

                api = get_api()
                account = api.get_account()
                equity = float(account.equity) 
                target_notional = 0.1 * equity # I decide to trade ten percent of my Alpaca equity.
                trading_our_choice(get_api(), target_etf, target_notional)
            else:
                print('There is not a valid signal date for today.')   
        else:
            print('Today is not the last trading day of the month.')
    else:
        print('The market is not closed yet.')
