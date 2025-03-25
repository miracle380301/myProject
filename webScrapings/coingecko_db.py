import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_
import requests
from model_db import Exchange
 
def coingecko_fetch_and_store_exchanges_db(db: Session):
     if db is None:
         raise ValueError("Database session is not initialized")
     
     try:
         url = "https://api.coingecko.com/api/v3/exchanges"
 
         headers = {
             "accept": "application/json",
             "x-cg-pro-api-key": "CG-LUDGRLmVaiHYyJXRrDtME2XE"
         }
 
         response = requests.get(url, headers=headers)
 
         if response.status_code == 200:
             exchanges_data = response.json()
             
             for exchange_data in exchanges_data:
                 name = exchange_data.get('name', 'N/A').lower()
                 year = exchange_data.get('year_established', 'N/A')
                 country = exchange_data.get('country', 'N/A')
                 url = exchange_data.get('url', 'N/A')
                 logo = exchange_data.get('image', 'N/A')
                 
                 # 중복 체크: 동일한 name 값이 있는지 확인
                 existing = db.query(Exchange).filter(
                     or_(
                         Exchange.name == name,
                     )
                 ).first()  # 첫 번째로 일치하는 항목을 찾습니다.
 
                 if existing:
                    # Update only the update_dt field
                    existing.update_dt = datetime.datetime.now()
                    db.commit()  # Commit the update
                    print(f"Updated existing exchange: {existing.name}")
                    continue
                 else:
                     new_exchange = Exchange(
                         name=name,
                         year=year,
                         country=country,
                         url=url,
                         logo=logo,
                         origin='coingecko',
                         create_dt = datetime.datetime.now(),
                         update_dt = datetime.datetime.now()
                      )
 
                     db.add(new_exchange)
                     db.commit()
                     print("새로운 exchange가 저장되었습니다:", new_exchange)
         else:
             print(f"Failed to fetch data from CoinGecko API. Status code: {response.status_code}")
         db.close()
     except Exception as e:
         print(f"Error : {e}")
         db.close()