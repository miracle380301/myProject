from sqlalchemy.orm import Session
from sqlalchemy import or_
import requests
from common.utils import check_name_exists, save_to_csv
from model1 import Exchange
import csv
import datetime

def coingecko_fetch_and_store_exchanges_csv(csv_file):
    if csv_file is None:
        raise ValueError("File doesn't exists.")
    
    try:
        url = "https://api.coingecko.com/api/v3/exchanges"

        headers = {
            "accept": "application/json",
            "x-cg-pro-api-key": "CG-LUDGRLmVaiHYyJXRrDtME2XE"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            exchanges_data = response.json()
            exchanges = []
            i = 1

            for exchange_data in exchanges_data:
                origin = 'ConinGecko'
                id = i
                name = exchange_data.get('name', 'N/A')
                year_established = exchange_data.get('year_established', 'N/A')
                country = exchange_data.get('country', 'N/A')
                url = exchange_data.get('url', 'N/A')
                logo_image = exchange_data.get('image', 'N/A')
                create_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                update_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                row_exchange = Exchange(origin=origin, id=id, name=name, year_established=year_established, country=country, url=url, logo_image=logo_image, create_dt=create_dt, update_dt=update_dt)

                # Check duplicate rows
                if check_name_exists(name, csv_file):
                    print(f"Exchange with name '{name}' already exists")
                    continue

                else:
                    exchanges.append(row_exchange)
                    i += 1
        
            #Save Data
            if exchanges is not None:
                save_to_csv(exchanges, csv_file)
        else:
            print(f"Failed to fetch data from CoinGecko API. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error : {e}")
