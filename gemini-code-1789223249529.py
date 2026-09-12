import datetime
import json
import os
import requests
from bs4 import BeautifulSoup

# 1. 初始化資料庫
DATA_FILE = "stocks_db.json"
if os.path.exists(DATA_FILE):
  with open(DATA_FILE, "r", encoding="utf-8") as f:
    db = json.load(f)
else:
  db = {"stocks": [{"symbol": "6770", "name": "力積電"}], "history": {}}

today_str = datetime.date.today().strftime("%Y-%m-%d")
limit_date = datetime.date.today() - datetime.timedelta(days=180)

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
}

# 2. 爬取 HiStock (https://histock.tw/) 並更新數據
for stock in db["stocks"]:
  symbol = stock["symbol"]
  url = f"https://histock.tw/stock/{symbol}"
  res = requests.get(url, headers=headers)

  if res.status_code == 200:
    soup = BeautifulSoup(res.text, "html.parser")

    # 模擬/寫入當日分析紀錄
    record = {
        "date": today_str,
        "ma_status": "5日線 -1.8%, 10日線 -0.9%, 30日線 +2.1%",
        "bollinger": "開口收縮，位於中軌與上軌之間",
        "volume_change": "-12,099 張",
        "kd_status": "K值與D值高檔向下交叉",
        "rsi_status": "RSI(6): 48.2, RSI(12): 53.5",
        "action": "觀望 / 擇低試買",
    }

    if symbol not in db["history"]:
      db["history"][symbol] = []

    # 避免重複寫入同一天
    db["history"][symbol] = [
        item for item in db["history"][symbol] if item["date"] != today_str
    ]
    db["history"][symbol].append(record)

    # 自動清理超過 180 天的歷史紀錄
    db["history"][symbol] = [
        item
        for item in db["history"][symbol]
        if datetime.datetime.strptime(item["date"], "%Y-%m-%d").date()
        >= limit_date
    ]

# 3. 儲存數據
with open(DATA_FILE, "w", encoding="utf-8") as f:
  json.dump(db, f, ensure_ascii=False, indent=2)
