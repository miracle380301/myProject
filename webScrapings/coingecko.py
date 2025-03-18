from sqlalchemy.orm import Session
from sqlalchemy import or_
import requests
from model import Exchange

def coingecko_fetch_and_store_exchanges(db: Session):
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
            print(exchanges_data)

            for exchange_data in exchanges_data:
                name = exchange_data.get('name', 'N/A')
                link = exchange_data.get('url', 'N/A')
                logo = exchange_data.get('image', 'N/A')

                # 중복 체크: 동일한 name, link, logo 값이 있는지 확인
                existing = db.query(Exchange).filter(
                    or_(
                        Exchange.name == name,
                    )
                ).first()  # 첫 번째로 일치하는 항목을 찾습니다.

                if existing:
                    continue
                else:
                    new_exchange = Exchange(
                        name=name,
                        link=link,
                        logo=logo,
                        origin='coingecko'
                    )

                    db.add(new_exchange)  # 세션에 추가
                    db.commit()  # DB에 커밋하여 저장
                    print("새로운 exchange가 저장되었습니다:", new_exchange)
        else:
            print(f"Failed to fetch data from CoinGecko API. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error : {e}")