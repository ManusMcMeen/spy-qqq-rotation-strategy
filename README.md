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
- **Matplotlib** – Performance visualization
- **dotenv** – Secure API key storage
- **Cron Jobs** – Automated monthly execution

## How to Run
1. Clone this repository:
   ```bash
   git clone https://github.com/YOURUSERNAME/spy-qqq-rotation-strategy.git
   cd spy-qqq-rotation-strategy

2.) Install dependencies:
pip install -r requirements.txt

3.) Create a .env file that contains your Alpaca API keys. Sample below:

ALPACA_API_KEY_ID=your_key

ALPACA_API_SECRET_KEY=your_secret

ALPACA_BASE_URL=https://paper-api.alpaca.markets

4.) Run the API checker and the backtest (with startdate of your choice).
Sample Results
(Backtest from 2010-01-01 to 2025-08-08)

--- Strategy Performance ---
CAGR: 13.76%
Volatility: 17.69%
Sharpe Ratio: 0.99

## Learning Objectives
API-based data acquisition
Portfolio performance metrics calculation
Rule-based investment strategy design
Automation of recurring tasks

## Disclaimer
This project is for educational purposes only. It is not financial advice, and past performance is not indicative of future results.
