# spy-qqq-rotation-strategy
Python backtest and automation script for a SPY/QQQ monthly rotation strategy using Alpaca API.

# SPY/QQQ Monthly Rotation Strategy

## Overview
This project implements a systematic trading strategy that rotates monthly between the S&P 500 ETF (**SPY**) and the Nasdaq-100 ETF (**QQQ**) based on their trailing 3-month performance. The goal is to capture momentum while limiting downside risk through a simple, rules-based allocation approach.

Although developed for personal learning, the methodology and backtesting process demonstrate skills in financial data analysis, performance evaluation, and basic automation.

## Strategy Logic
1. **Lookback Period**: 63 trading days (~3 months)
2. **Selection Rule**:  
   - At each month-end, calculate the total return of SPY and QQQ over the lookback period.
   - Invest 100% in the ETF with the higher return for the following month.
3. **Rebalancing**: Monthly, on the last trading day.
4. **Metrics Tracked**:
   - Compound Annual Growth Rate (CAGR)
   - Sharpe Ratio
   - Annualized Volatility

## Technology Stack
- **Python 3**
- **Pandas / NumPy** – Data handling & calculations
- **Alpaca API** – Historical price data and order management
  -  Create account/sign up for Alpaca API and paper trading on https://alpaca.markets/.
  -  On the home page, generate your API keys. These will go into your .env file.
- **Matplotlib** – Performance visualization
- **dotenv** – Secure API key storage
- **Cron Jobs** – Automated monthly execution

## How to Run

1. Clone this repository
   ```bash
   git clone https://github.com/YOURUSERNAME/spy-qqq-rotation-strategy.git
   cd spy-qqq-rotation-strategy
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a .env file that contains your Alpaca API keys. Sample below:
   ```bash
   ALPACA_API_KEY_ID=your_key

   ALPACA_API_SECRET_KEY=your_secret

   ALPACA_BASE_URL=https://paper-api.alpaca.markets
   ```
4. Run the API checker and the backtest (with startdate of your choice).
   ``` bash
   python api_checker.py
   ```
   ``` bash
   python backtester.py
   ```
   
   Sample Results
   
   (Backtest from 2023-01-01 to 2025-08-07)

   CAGR: 17.39%
   Volatility: 15.95%
   Sharpe Ratio: 1.29
5. Trade execution.
**Optional: Schedule in cron**
Run on final trading day of the month after 4p.m ET.

## Learning Objectives
API-based data acquisition
Portfolio performance metrics calculation
Rule-based investment strategy design
Automation of recurring tasks

## To-do
-- **Killswitch**
-- **Issues with backtester before '2016-02-29'**
-- **Multi-signal approach**

## Disclaimer
This project is for educational purposes only. It is not financial advice, and past performance is not indicative of future results.
