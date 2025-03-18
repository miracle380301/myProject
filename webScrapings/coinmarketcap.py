from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from sqlalchemy import or_
from model import Exchange

def coinmarketcap_fetch_and_store_exchanges(db: Session):
    if db is None:
        raise ValueError("Database session is not initialized")
    
    # Selenium 설정
    options = Options()
    options.headless = True  # 브라우저 창을 띄우지 않음
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # 웹사이트 열기
    driver.get("https://coinmarketcap.com/rankings/exchanges/")

    # 페이지가 완전히 로드될 때까지 대기 (예시로 5초 대기)
    time.sleep(5)

    # "Show More" 버튼을 클릭
    try:
        show_more_button = driver.find_element(By.XPATH, '//button[text()="Show More"]')
        show_more_button.click()
        time.sleep(15)  # 추가 데이터를 로딩할 시간을 기다립니다.
    except Exception as e:
        print(f"Error clicking 'Show More' button: {e}")

    # HTML 가져오기
    html = driver.page_source

    URL = "https://coinmarketcap.com/rankings/exchanges/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(html, "html.parser")
        exchanges = soup.select("table tbody tr")

        for exchange in exchanges:  # 상위 10개만 저장
            # Find all exchange rows in the table
            exchanges = []
            for row in soup.select("table tbody tr"):
                # Extract name
                name_tag = row.select_one("td:nth-child(2) a")
                exchange.name = name_tag.text.strip() if name_tag else "N/A"

                # Extract link
                exchange.link = "https://coinmarketcap.com" + name_tag["href"] if name_tag else "N/A"

                # Extract icon (logo image)
                icon_tag = row.select_one("td:nth-child(2) img")
                exchange.logo = icon_tag["src"] if icon_tag else "N/A"
                
                # 중복 체크: 동일한 name, link, logo 값이 있는지 확인
                existing = db.query(Exchange).filter(
                    or_(
                        Exchange.name == exchange.name,
                        Exchange.link == exchange.link,
                        Exchange.logo == exchange.logo
                    )
                ).first()  # 첫 번째로 일치하는 항목을 찾습니다.
                
                if existing:
                    continue
                else: 
                    new_exchange = Exchange(
                        name=exchange.name,
                        link=exchange.link,
                        logo=exchange.logo
                    )

                    db.add(new_exchange)  # 세션에 추가
                    db.commit()  # DB에 커밋하여 저장
                    print("새로운 exchange가 저장되었습니다:", new_exchange)
        driver.quit()