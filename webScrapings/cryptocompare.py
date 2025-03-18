from sqlalchemy.orm import Session
from sqlalchemy import or_
import requests
from model import Exchange

def crytocompare_fetch_and_store_exchanges(db: Session):
    if db is None:
        raise ValueError("Database session is not initialized")
    
    try:
        url = "https://min-api.cryptocompare.com/data/exchanges/general"
        api_key = "6ffb33fc547ff77395721efad05a1445b9f2b09cfdd28c3400e3e9bfd867fbb9"

        headers = {"Authorization": f"Bearer {api_key}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            exchanges_data = response.json().get('Data', {})
            #print(exchanges_data)

            for exchange_id, exchange_data in exchanges_data.items():
                name = exchange_data.get('Name', 'N/A')
                link = "https://www.cryptocompare.com" + exchange_data.get('Url', 'N/A')
                logo = "https://www.cryptocompare.com" + exchange_data.get('LogoUrl', 'N/A')

                # 중복 체크: 동일한 name, link, logo 값이 있는지 확인
                existing = db.query(Exchange).filter(
                    or_(
                        Exchange.name == name,
                        Exchange.link == link,
                        Exchange.logo == logo
                    )
                ).first()  # 첫 번째로 일치하는 항목을 찾습니다.

                if existing:
                    continue
                else:
                    new_exchange = Exchange(
                        name=name,
                        link=link,
                        logo=logo,
                        origin='cryptocompare'
                    )

                    db.add(new_exchange)  # 세션에 추가
                    db.commit()  # DB에 커밋하여 저장
                    print("새로운 exchange가 저장되었습니다:", new_exchange)
        else:
            print(f"Failed to fetch data from CryptoCompare API. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error : {e}")