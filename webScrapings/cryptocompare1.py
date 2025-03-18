import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_
import requests
from common.utils import check_name_exists, save_to_csv
from model1 import Exchange
import csv
import re


def crytocompare_fetch_and_store_exchanges_csv(csv_file):
    if csv_file is None:
        raise ValueError("File doesn't exists.")
    
    try:
        url = "https://min-api.cryptocompare.com/data/exchanges/general"
        api_key = "6ffb33fc547ff77395721efad05a1445b9f2b09cfdd28c3400e3e9bfd867fbb9"

        headers = {"Authorization": f"Bearer {api_key}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            exchanges_data = response.json().get('Data', {})
            exchanges = []

            with open(csv_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                max_id = max((int(row['id']) for row in reader), default=0)
                i = max_id + 1
            
            for exchange_data in exchanges_data.items():
                #print('@exchange_data', exchange_data[1])
                origin = 'CryptoCompare'
                id = i
                name = exchange_data[1].get('Name', 'N/A')
                match = re.search(r"20\d{2}", exchange_data[1].get('Description', 'N/A'))
                if match: 
                    year_established = match.group(0) 
                else: 
                    year_established ='N/A'
                country = exchange_data[1].get('Country', 'N/A')
                url = exchange_data[1].get('AffiliateURL', 'N/A')
                logo_image = 'https://www.cryptocompare.com/'+exchange_data[1].get('LogoUrl', 'N/A')
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

