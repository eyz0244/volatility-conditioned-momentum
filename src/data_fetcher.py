# src/data_fetcher.py

import os
import requests
import time
from typing import Dict

def fetch_and_save_price(
    ticker: str,
    config: Dict[str, str],
    log_path: str = "pull_log.txt",
    max_retries: int = 3,
    sleep_secs: int = 5
) -> None:
    """
    Fetch historical EOD price data for a ticker and save to CSV.

    Parameters:
        ticker (str): Ticker symbol.
        config (dict): Contains API and directory parameters.
        log_path (str): Log file for failed downloads.
        max_retries (int): Retry attempts on failure.
        sleep_secs (int): Delay between retries.
    """
    out_path = os.path.join(config["OUTPUT_DIR"], f"{ticker}.csv")

    # Skip download if file already exists
    if os.path.exists(out_path):
        print(f"SKIPPED (exists): {ticker}")
        return

    # Define API query parameters
    params = {
        "api_token": config["API_KEY"],
        "fmt": "csv",
        "from": config["DATE_FROM"],
        "to": config["DATE_TO"]
    }
    url = f"{config['BASE_URL']}/{ticker}"

    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)

            # Rate limiting — retry
            if response.status_code == 429:
                print("Rate limit reached. Retrying...")
                time.sleep(sleep_secs)
                continue

            # Success — save file
            if response.status_code == 200 and len(response.text) > 100:
                with open(out_path, "w") as f:
                    f.write(response.text)
                return

            # Failure — log status
            with open(log_path, "a") as log:
                log.write(f"FAILED [{response.status_code}]: {ticker}\n")
            return

        except Exception as e:
            # Log error
            with open(log_path, "a") as log:
                log.write(f"ERROR: {ticker} – {str(e)}\n")
            print(f"Error: {ticker} – {str(e)}")
            time.sleep(sleep_secs)
