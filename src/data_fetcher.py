# src/data_fetcher.py

import os
import requests

def fetch_and_save_price(ticker, exchange_file, BASE_URL, API_KEY, DATE_FROM, DATE_TO, OUTPUT_DIR, log_path="pull_log.txt"):
    """
    Fetch historical EOD price data for a ticker and save to CSV.

    Parameters:
        ticker (str): Ticker symbol.
        exchange_file (str): Source file where ticker came from (used for logging).
        log_path (str): Path to the log file for failed downloads.
    """
    out_path = f"{OUTPUT_DIR}/{ticker}.csv"
    if os.path.exists(out_path):
        print(f"SKIPPED (exists): {ticker}")
        return

    params = {
        "api_token": API_KEY,
        "fmt": "csv",
        "from": DATE_FROM,
        "to": DATE_TO
    }
    url = f"{BASE_URL}/{ticker}"

    try:
        response = requests.get(url, params=params)

        if response.status_code == 429:
            print("Rate limit reached. Aborting.")
            raise SystemExit

        if response.status_code == 200 and len(response.text) > 100:
            with open(out_path, "w") as f:
                f.write(response.text)
        else:
            with open(log_path, "a") as log:
                log.write(f"FAILED [{response.status_code}]: {ticker} from {exchange_file}\n")
    except Exception as e:
        with open(log_path, "a") as log:
            log.write(f"ERROR: {ticker} – {str(e)}\n")
        print(f"Error: {ticker} – {str(e)}")