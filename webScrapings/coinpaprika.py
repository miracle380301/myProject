import csv
import re
import requests
from common.utils import check_name_exists, save_to_csv
from model import Exchange
import datetime

def coinpaprika_fetch_and_store_exchanges_csv(csv_file):
    if csv_file is None:
        raise ValueError("File doesn't exists.")
    
    try:
        url = "https://api.coinpaprika.com/v1/exchanges"

        response = requests.get(url)

        if response.status_code == 200:
            exchanges_data = response.json()
            exchanges = []

            with open(csv_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                max_id = max((int(row['id']) for row in reader), default=0)
                i = max_id + 1
            
            for exchange_data in exchanges_data:
                origin = 'Coinpaprika'
                if exchange_data.get('active') == True:
                    id = i
                    name = exchange_data.get('name', 'N/A')
                    description = exchange_data.get('description', '')
                    if description is None:
                        description = ''
                    match = re.search(r"20\d{2}", description)
                    if match: 
                        year_established = match.group(0) 
                    else: 
                        year_established ='N/A'
                    country = exchange_data.get('country', 'N/A')
                    links = exchange_data.get('links', {})
                    url = links.get('website', ['N/A'])[0] if links else 'N/A'  # Get the first website link
                    logo_image = exchange_data.get('image', 'N/A')
                    if logo_image == 'N/A':
                        logo_image = 'static/images/nodata.png'  # Set default image path
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
            print(f"Failed to fetch data from Coinpaprika API. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error : {e}")
