import ccxt
import requests
from common.utils import check_name_exists, save_to_csv
from model import Exchange
import datetime

def ccxt_fectch_and_store_exchanges_csv(csv_file):
    if csv_file is None:
        raise ValueError("File doesn't exists.")
    
    exchanges = ccxt.exchanges  # 거래소 리스트 가져오기
    print(exchanges)
    return exchanges

