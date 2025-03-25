import datetime
import re
from sqlalchemy.orm import Session
from sqlalchemy import or_
import requests
from model_db import Exchange
 
def crytocompare_fetch_and_store_exchanges_db(db: Session):
     if db is None:
         raise ValueError("Database session is not initialized")
     
     try:
         url = "https://min-api.cryptocompare.com/data/exchanges/general"
         api_key = "6ffb33fc547ff77395721efad05a1445b9f2b09cfdd28c3400e3e9bfd867fbb9"
 
         headers = {"Authorization": f"Bearer {api_key}"}
 
         response = requests.get(url, headers=headers)
 
         if response.status_code == 200:
             exchanges_data = response.json().get('Data', {})
             print(exchanges_data)
 
             for exchange_data in exchanges_data.values():
                 name = exchange_data.get('Name', 'N/A').lower()
                 match = re.search(r"20\d{2}", exchange_data.get('Description', 'N/A'))
                 if match: 
                    year_established = match.group(0) 
                 else: 
                    year_established ='N/A'
                 year = year_established
                 country = exchange_data.get('Country', 'N/A')
                 url = exchange_data.get('AffiliateURL', 'N/A')
                 # Check if LogoUrl exists and prepend the base URL
                 logo_url = exchange_data.get('LogoUrl', None)
                 if logo_url:
                    logo = f"https://www.cryptocompare.com/{logo_url}"
                 else:
                    logo = 'N/A'
 
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
                         origin='cryptocompare',
                         create_dt = datetime.datetime.now(),
                         update_dt = datetime.datetime.now()
                      )
 
                     db.add(new_exchange)  # 세션에 추가
                     db.commit()  # DB에 커밋하여 저장
                     print("새로운 exchange가 저장되었습니다:", new_exchange)
         else:
             print(f"Failed to fetch data from CryptoCompare API. Status code: {response.status_code}")
         db.close()
     except Exception as e:
         print(f"Error : {e}")
         db.close()