from database import get_db
from webScrapings.coingecko_db import coingecko_fetch_and_store_exchanges_db
from webScrapings.cryptocompare_db import crytocompare_fetch_and_store_exchanges_db

def fetch_and_store():
    """Fetch and store data from CoinGecko and CryptoCompare."""
    with next(get_db()) as db:  # Get a database session
        print("Starting CoinGecko fetch and store...")
        coingecko_fetch_and_store_exchanges_db(db)
        print("CoinGecko fetch and store completed.")

        print("Starting CryptoCompare fetch and store...")
        crytocompare_fetch_and_store_exchanges_db(db)
        print("CryptoCompare fetch and store completed.")
if __name__ == "__main__":
    fetch_and_store()