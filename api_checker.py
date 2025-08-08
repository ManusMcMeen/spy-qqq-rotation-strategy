# Imports: # pip install alpaca-trade-api python-dotenv pandas numpy python-dateutil

import os 
from dotenv import load_dotenv
from alpaca_trade_api import REST

# Checks API 

def get_api():
    load_dotenv()  # reads .env 
    base = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")
    key  = os.getenv("ALPACA_API_KEY_ID")
    sec  = os.getenv("ALPACA_API_SECRET_KEY")

    # Safety checks
    if not key or not sec:
        print('Missing API keys. Put them in an .env file as ALPACA_API_KEY_ID and ALPACA_API_SECRET_KEY.')
    return REST(key_id=key, secret_key=sec, base_url=base)

def main():
    api = get_api()
    acct = api.get_account()
    print('Connected to Alpaca PAPER account!')
    print('Equity:', acct.equity)

if __name__ == "__main__":
    main()
