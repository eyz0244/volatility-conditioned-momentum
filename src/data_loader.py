# src/data_loader.py

import pandas as pd
import os

def load_price_data(price_dir):
    """
    Load individual ticker files into a single wide-format price DataFrame.
    Assumes each file contains 'date' and 'adj_close' columns.
	
    Parameters:
        price_dir (str): Folder where raw prices are saved
    """

    files = [f for f in os.listdir(price_dir) if f.endswith('.csv') or f.endswith('.parquet')]
    price_dfs = []

    for file in files:
        ticker = file.split('.')[0] # Split ticker and get ticker name
        path = os.path.join(price_dir, file) # Set file path
        df = pd.read_parquet(path) if file.endswith('.parquet') else pd.read_csv(path)
        df.columns = ['date','open','high','low','close','adj_close','volume'] # Rename columns for downstream function use
        df = df[['date', 'adj_close']].copy() # Subset date and adj_close
        df['date'] = pd.to_datetime(df['date']) # Convert date to datetime
        df = df.set_index('date').rename(columns={'adj_close': ticker}) # Set date as index
        price_dfs.append(df) # Append ticker df

    price_wide = pd.concat(price_dfs, axis=1).sort_index() # Concat all dfs together
    return price_wide