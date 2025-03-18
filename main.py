import datetime
import os
from ssl import Options
from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from flask import render_template
from sqlalchemy import create_engine, or_, text
from sqlalchemy.orm import Session

from common.utils import get_exchange_list
from database import SessionLocal, engine
from model import Exchange
from model1 import Exchange
from sqlalchemy.orm import sessionmaker
import pymysql

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from webScrapings.coingecko import coingecko_fetch_and_store_exchanges
from webScrapings.coingecko1 import coingecko_fetch_and_store_exchanges_csv
from webScrapings.coinmarketcap import coinmarketcap_fetch_and_store_exchanges
from webScrapings.coinmarketcap1 import coinmarketcap_fetch_and_store_exchanges_csv
from webScrapings.cryptocompare import crytocompare_fetch_and_store_exchanges

import csv
from pathlib import Path

from webScrapings.cryptocompare1 import crytocompare_fetch_and_store_exchanges_csv

app = FastAPI()
templates = Jinja2Templates(directory="templates")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 디렉토리
csv_file_path = os.path.join(BASE_DIR, "__pycache__", "files", "exchanges.csv")

# DB 세션의존성
def get_db():
    
    # conn = pymysql.connect(host='127.0.0.1',user='root',passwd='135135',db='mysql')
    # try:
    #     cur = conn.cursor()
    #     cur.execute("USE crypto")
    #     cur.execute("SELECT * FROM exchanges")
    #     print(cur.fetchall())
    #     print("✅ Successfully connected to MySQL!")
    
    # finally:        
    #     conn.close()
    # return conn
    engine = create_engine("mysql+pymysql://root:135135@localhost/crypto")
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


@app.get("/")
async def home(request: Request, db : Session = Depends(get_db)):
    #coinmarketcap_fetch_and_store_exchanges(db)  # coinmarketcap 크롤링 & DB 저장
    #coingecko_fetch_and_store_exchanges(db) # coingecko 크롤링 & DB 저장
    #crytocompare_fetch_and_store_exchanges(db) # cryptocompare 크롤링 & DB 저장

    #coingecko_fetch_and_store_exchanges_csv(csv_file_path) #coingecko 크롤링 & File 저장
    #crytocompare_fetch_and_store_exchanges_csv(csv_file_path) # cryptocompare 크롤링 & File 저장
    #coinmarketcap_fetch_and_store_exchanges_csv(csv_file_path)  # coinmarketcap 크롤링 & File 저장    
    
    #exchanges = db.query(Exchange).all()  # 저장된 거래소 가져오기
    exchanges = get_exchange_list(csv_file_path)
    
    return templates.TemplateResponse("index.html", {"request": request, "exchanges": exchanges})

@app.post("/")
async def index(request: Request):
    keyword = await request.form()
    keyword = keyword.get("keyword")
    exchanges = []
    with open(csv_file_path, "r", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if keyword.lower() in row["name"].lower():
                exchanges.append(row)

    if not exchanges:
        no_result_message = "There is no data."
    else:
        no_result_message = ""

    return templates.TemplateResponse("index.html", {"request": request, "exchanges": exchanges, "keyword": keyword, "no_result_message": no_result_message})

# async def index(request: Request, search_query: str = None, db: Session = Depends(get_db)):
#     # 거래소 찾기 (이름이 검색어와 일치하는 거래소)
#     if search_query:
#         results = db.query(Exchange).filter(Exchange.name.ilike(f"%{search_query}%")).all()
#         print('results=', results)
#     else:
#         results = db.query(Exchange).all()  # 아무 검색어 없으면 모든 거래소를 보여줌
    
#     # 거래소가 없을 경우 메시지 설정
#     if not results and search_query:
#         no_result_message = "찾으시는 거래소가 없습니다."
#     else:
#         no_result_message = ""

#     # 템플릿 렌더링
#     return templates.TemplateResponse("index.html", {
#         "request": request,
#         "exchanges": results,
#         "search_query": search_query,
#         "no_result_message": no_result_message
#     })

