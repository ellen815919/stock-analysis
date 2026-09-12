import datetime
import json
import os
import requests
from bs4 import BeautifulSoup

# 1. 讀取現有股票清單與歷史資料
DATA_FILE = "stocks_db.json"
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)
else:
    db = {"stocks": ["2330"], "history": {}}

today_str = datetime.date.today().strftime("%Y-%m-%d")
limit_date = datetime.date.today() - datetime.timedelta(days=180)

# 2. 爬取 HiStock 數據與 180 天資料清理
for symbol in db["stocks"]:
    url = f"https://histock.tw/stock/{symbol}"
    # 使用 BeautifulSoup 解析 HiStock 的收盤價、MA、布林、成交量、KD、RSI
    # (此處可對接 OpenAI/Gemini API 產生每日建議)

    # 清理超過 180 天的歷史紀錄
    if symbol in db["history"]:
        db["history"][symbol] = [
            item
            for item in db["history"][symbol]
            if datetime.datetime.strptime(item["date"], "%Y-%m-%d").date()
            >= limit_date
        ]

# 3. 儲存更新後的資料庫
with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)