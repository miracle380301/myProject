import gettext
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from flask_babel import _

from webScrapings.ccxt import ccxt_fectch_and_store_exchanges_csv
from webScrapings.coingecko import coingecko_fetch_and_store_exchanges_csv
from webScrapings.coinmarketcap import coinmarketcap_fetch_and_store_exchanges_csv
from webScrapings.coinpaprika import coinpaprika_fetch_and_store_exchanges_csv
from webScrapings.cryptocompare import crytocompare_fetch_and_store_exchanges_csv

import csv

app = FastAPI()
templates = Jinja2Templates(directory="templates")

ITEMS_PER_PAGE = 15 # 한 페이지당 보여지는 리스트 수
LOCALE_DIR = "locales" # 번역 파일 경로 설정

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 디렉토리
csv_file_path = os.path.join(BASE_DIR, "__pycache__", "files", "exchanges.csv")
app.mount("/static", StaticFiles(directory="static"), name="static") # 이미지 파일

COINGECKO_UPDATE_DATE = None # 최신 업데이트 날짜
CRYPTOCOMPARE_UPDATE_DATE = None
COINPAPRIKA_UPDATE_DATE = None

# 번역 객체 생성 (기본 언어: 영어)
def get_translation(lang: str):
    return gettext.translation("messages", localedir=LOCALE_DIR, languages=[lang], fallback=True)

@app.middleware("http")
async def set_language(request: Request, call_next):
    # 쿠키 또는 쿼리에서 언어 설정 가져오기 (기본값: 영어)
    lang = request.cookies.get("language", "en")
    request.state.trans = get_translation(lang)
    response = await call_next(request)
    return response

@app.get("/")
async def home(request: Request):
    
    _ = request.state.trans.gettext  # 번역 함수 가져오기

    #coingecko_fetch_and_store_exchanges_csv(csv_file_path) #coingecko 크롤링 & File 저장 - 1
    #crytocompare_fetch_and_store_exchanges_csv(csv_file_path) # cryptocompare 크롤링 & File 저장 2
    #coinmarketcap_fetch_and_store_exchanges_csv(csv_file_path)  # coinmarketcap 크롤링 & File 저장    
    #coinpaprika_fetch_and_store_exchanges_csv(csv_file_path)  # coinpaprika 크롤링 & File 저장
    #ccxt_fectch_and_store_exchanges_csv(csv_file_path) # ccxt 크롤링 & File 저장
    
    exchanges = get_exchange_list(csv_file_path)
    
    # 🔹 페이징 처리
    page = int(request.query_params.get("page", 1))  # 기본값 1
    
    total_exchanges = len(exchanges)
    total_pages = (total_exchanges + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE  # 전체 페이지 수

    start_idx = (page - 1) * ITEMS_PER_PAGE
    end_idx = min(start_idx + ITEMS_PER_PAGE, total_exchanges)

    return templates.TemplateResponse(
                                        "index.html", 
                                        {
                                            "request": request, 
                                            "exchanges": exchanges, 
                                            "page": page, 
                                            "total_pages": total_pages, 
                                            "start_idx": start_idx, 
                                            "end_idx": end_idx,
                                            "coingecko_update_date":COINGECKO_UPDATE_DATE, 
                                            "cryptocompare_update_date":CRYPTOCOMPARE_UPDATE_DATE,
                                            "coinpaprika_update_date":COINPAPRIKA_UPDATE_DATE, 
                                            
                                            "gettext": _
                                        }
                                    )

def get_exchange_list(file_path):
    global COINGECKO_UPDATE_DATE, CRYPTOCOMPARE_UPDATE_DATE, COINPAPRIKA_UPDATE_DATE

    exchange_list = []
    latest_update = {
        'coingecko': None,
        'cryptocompare': None,
        'coinpaprika': None,
    }

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['origin','id', 'name', 'year_established','country','url','logo_image','create_dt', 'update_dt'])
        next(reader, None)
        for row in reader:
            exchange_list.append(row)

            origin = row['origin'].strip().lower()
            update_dt = row['update_dt'].strip()

            # 각 origin별 첫 번째 update_dt 값만 저장 (이미 값이 있으면 건너뜀)
            if origin in latest_update and latest_update[origin] is None:
                latest_update[origin] = update_dt
        
            # 최신 업데이트 날짜 변수 설정
            COINGECKO_UPDATE_DATE = latest_update['coingecko']
            CRYPTOCOMPARE_UPDATE_DATE = latest_update['cryptocompare']
            COINPAPRIKA_UPDATE_DATE = latest_update['coinpaprika']

    return exchange_list

@app.post("/")
async def index(request: Request):
    _ = request.state.trans.gettext  # 번역 함수 가져오기

    form_data = await request.form()
    keyword = form_data.get("keyword", "").strip().lower()  # 문자열로 변환

    exchanges = []
    with open(csv_file_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row.get("name", "")  # "name" 키가 없을 경우 기본값 "" 사용
            if keyword and keyword in name.lower():
                exchanges.append(row)

    no_result_message = "no_result" if not exchanges else ""

    # 🔹 페이징 처리
    page = int(1)  # 기본값 1
    total_exchanges = len(exchanges)
    total_pages = (total_exchanges + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE  # 전체 페이지 수

    start_idx = (page - 1) * ITEMS_PER_PAGE
    end_idx = min(start_idx + ITEMS_PER_PAGE, total_exchanges)
    paginated_exchanges = exchanges[start_idx:end_idx]  # 해당 페이지의 데이터만 전달

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "exchanges": paginated_exchanges,
            "keyword": keyword,
            "no_result_message": no_result_message,
            "page": page, 
            "total_pages": total_pages, 
            "start_idx": start_idx, 
            "end_idx": end_idx,
            "coingecko_update_date":COINGECKO_UPDATE_DATE, 
            "cryptocompare_update_date":CRYPTOCOMPARE_UPDATE_DATE,
            "coinpaprika_update_date":COINPAPRIKA_UPDATE_DATE, 
            "gettext": _
        },
    )

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    _ = request.state.trans.gettext  # 번역 함수 가져오기
    return templates.TemplateResponse("about.html", {"request": request, "gettext": _})

@app.get("/privacy", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})

@app.get("/history", response_class=HTMLResponse)
async def about(request: Request):
    _ = request.state.trans.gettext  # 번역 함수 가져오기
    return templates.TemplateResponse("history.html", {"request": request, "gettext": _})