import csv
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup
from common.utils import check_name_exists, save_to_csv
from model import Exchange
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def coinmarketcap_fetch_and_store_exchanges_csv(csv_file):
    if csv_file is None:
        raise ValueError("File doesn't exists.")
    
    # Selenium 설정
    options = Options()
    options.headless = True  # 브라우저 창을 띄우지 않음
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # 웹사이트 열기
    driver.get("https://coinmarketcap.com/rankings/exchanges/")

    # 페이지가 완전히 로드될 때까지 대기 (예시로 5초 대기)
    time.sleep(15)

    try:
        show_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Show More"]'))
        )
        show_more_button.click()

        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
        )  # 모든 거래소가 로드될 때까지 기다림

        time.sleep(5)  # 추가 대기
    except Exception as e:
        print(f"Error clicking 'Show More' button: {e}")

    # HTML 가져오기
    html = driver.page_source

    try : 
        URL = "https://coinmarketcap.com/rankings/exchanges/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(URL, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(html, "html.parser")
            exchanges = soup.select("table tbody tr")

            exchanges_array = []

            for exchange in exchanges:
                # Find all exchange rows in the table
                
                with open(csv_file, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    max_id = max((int(row['id']) for row in reader), default=0)
                    i = max_id + 1

                #for exchange_data in soup.select("table tbody tr"):
                    origin = 'CoinMarketCap'
                    id = i
                    # Extract name
                    name_tag = exchange.select_one("td:nth-child(2) a")
                    name = name_tag.text.strip() if name_tag else "N/A"

                    # Extract link
                    url = "https://coinmarketcap.com" + name_tag["href"] if name_tag else "N/A"

                    # Extract icon (logo image)
                    icon_tag = exchange.select_one("img.coin-logo, td:nth-child(2) img")
                    logo_image = icon_tag["src"] if icon_tag else "N/A"

                    year_established = 'N/A'
                    country = 'N/A'
                    create_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    update_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    row_exchange = Exchange(origin=origin, id=id, name=name, year_established=year_established, country=country, url=url, logo_image=logo_image, create_dt=create_dt, update_dt=update_dt)
                    
                    if not any(e.name == name for e in exchanges_array) and not check_name_exists(name, csv_file):
                        exchanges_array.append(row_exchange)
                        i += 1                    
            
            #Save Data
            if exchanges_array:
                save_to_csv(exchanges_array, csv_file)
        else:
            print(f"Failed to fetch data from CoinMarketCap API. Status code: {response.status_code}")
        
        driver.quit()
    except Exception as e:
        print(f"Error : {e}")
