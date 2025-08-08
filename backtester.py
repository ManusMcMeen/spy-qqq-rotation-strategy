# Imports

import os
import time
import numpy as np
import pandas as pd
from pandas.tseries.offsets import BMonthEnd
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from alpaca_trade_api import REST, TimeFrame
import matplotlib.pyplot as plt

TICKERS = ['SPY', 'QQQ']
lookback_time = 63 # Around 3 months worth of trading days
backtest_start_date = '2023-01-01'
risk_free_rate = 0.02

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
    end = end or (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    frames = []
    for sym in symbols:
        bars = api.get_bars(sym, TimeFrame.Day, start, end, limit=50000).df
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
    
    print("First signal date (after shift):", choice_series.dropna().index.min())
    print("Last signal date:", choice_series.dropna().index.max())
    choice = choice_series.shift(1)
    return choice 

# Backtest function

def backtest_strategy(prices, choice_series, risk_free_rate):
    monthly_returns = prices.pct_change().resample('ME').apply(lambda x: (1 + x).prod() - 1)
    
    # Normalize indices to align
    monthly_returns.index = monthly_returns.index.normalize()
    choice_series.index = choice_series.index.normalize()

    strategy_returns = []
    for date in choice_series.index:
        choice = choice_series.loc[date]
        if pd.isna(choice):
            strategy_returns.append(np.nan)
        elif date in monthly_returns.index and choice in monthly_returns.columns:
            strategy_returns.append(monthly_returns.loc[date, choice])
        else:
            strategy_returns.append(np.nan)

    strategy_returns = pd.Series(strategy_returns, index=choice_series.index, name='strategy_return').dropna()
    cumulative = (1 + strategy_returns).cumprod()

    total_return = cumulative.iloc[-1] - 1
    num_years = (strategy_returns.index[-1] - strategy_returns.index[0]).days / 365.25
    cagr = (1 + total_return) ** (1 / num_years) - 1
    volatility = strategy_returns.std() * np.sqrt(12)
    sharpe = (strategy_returns.mean() * 12 - risk_free_rate) / volatility

    print('\n--- Strategy Performance ---')
    print(f'CAGR: {cagr:.2%}')
    print(f'Volatility: {volatility:.2%}')
    print(f'Sharpe Ratio: {sharpe:.2f}')

    print("Strategy window:", strategy_returns.index.min().date(), "->", strategy_returns.index.max().date())
    print("n months:", strategy_returns.shape[0])
    cumulative.plot(title='Strategy Cumulative Return', figsize=(10, 5))
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Main
if __name__ == '__main__':
    api = get_api()
    prices = daily_close_prices(api, TICKERS, backtest_start_date, end=None)

    choice = monthly_choice(prices)

    backtest_strategy(prices, choice, risk_free_rate)
    
