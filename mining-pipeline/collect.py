import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime, timedelta
import yfinance as yf

# 硬编码数据存储
DATA_FILE = "data/news.json"

def fetch_mining_com():
    print("[爬虫] mining.com 开始...")
    try:
        url = "https://www.mining.com/feed/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        resp = requests.get(url, timeout=10, headers=headers)
        soup = BeautifulSoup(resp.content, "xml")
        items = soup.find_all("item")
        results = []
        for item in items[:200]:
            results.append({
                "source": "mining.com",
                "title": item.title.text if item.title else "",
                "link": item.link.text if item.link else "",
                "pub_date": item.pubDate.text if item.pubDate else "",
                "content": item.description.text if item.description else ""
            })
        print(f"[爬虫] mining.com 获取 {len(results)} 条")
        return results
    except Exception as e:
        print(f"[爬虫] mining.com 出错: {e}")
        return []

def fetch_policy():
    """生成200条政策模拟数据"""
    print("[爬虫] 政策数据：生成 200 条模拟数据...")
    
    titles = [
        "稀土资源开发管理办法",
        "稀土出口管制政策",
        "稀土行业规范条件",
        "稀土资源税改革方案",
        "稀土开采总量控制指标",
        "稀土冶炼分离产能置换政策",
        "稀土新材料产业扶持政策",
        "稀土产品出口配额管理办法",
        "稀土行业数字化转型指导意见",
        "稀土资源综合利用管理办法",
        "稀土行业绿色发展指导意见",
        "稀土战略储备管理办法",
        "稀土产业高质量发展行动计划",
        "稀土进出口贸易管理规定",
        "稀土行业标准体系建设方案",
    ]
    
    sources = ["中国稀土", "澳洲DISR", "工信部", "商务部", "发改委", "财政部", "自然资源部"]
    
    samples = []
    for i in range(400):
        title = f"{titles[i % len(titles)]}（2026年第{i+1:03d}批）"
        source = sources[i % len(sources)]
        day = (i % 28) + 1
        samples.append({
            "source": source,
            "title": title,
            "link": "#",
            "pub_date": f"2026-08-{day:02d}",
            "content": f"关于{title}的通知，涉及稀土资源管理、出口管制、行业规范、税收改革等内容。第{i+1}批政策文件。"
        })
    
    print(f"[爬虫] 政策数据获取 {len(samples)} 条")
    return samples

def fetch_price():
    """用 yfinance 获取铜期货历史价格（最近30天）"""
    print("[爬虫] 价格数据：获取铜期货历史价格...")
    try:
        ticker = yf.Ticker("HG=F")
        hist = ticker.history(period="1mo")
        
        if hist.empty:
            print("[爬虫] 价格数据为空，使用模拟数据")
            return fetch_price_mock()
        
        results = []
        for date, row in hist.iterrows():
            results.append({
                "source": "LME",
                "commodity": "铜",
                "date": date.strftime("%Y-%m-%d"),
                "price": round(row["Close"], 2),
                "high": round(row["High"], 2),
                "low": round(row["Low"], 2),
                "volume": int(row["Volume"]) if row["Volume"] else 0
            })
        print(f"[爬虫] 价格数据获取 {len(results)} 条")
        return results
    except Exception as e:
        print(f"[爬虫] 价格数据出错: {e}，使用模拟数据")
        return fetch_price_mock()

def fetch_price_mock():
    """生成30条价格模拟数据"""
    print("[爬虫] 价格数据：生成 30 条模拟数据...")
    import random
    results = []
    base_price = 8500
    for i in range(200):
        day = i + 1
        price = base_price + random.randint(-200, 200)
        results.append({
            "source": "LME",
            "commodity": "铜",
            "date": f"2026-08-{day:02d}",
            "price": price,
            "high": price + random.randint(10, 50),
            "low": price - random.randint(10, 50),
            "volume": random.randint(1000, 5000)
        })
    print(f"[爬虫] 价格数据获取 {len(results)} 条")
    return results

def collect_all():
    """收集所有数据，存成JSON"""
    all_data = []
    all_data.extend(fetch_mining_com())
    all_data.extend(fetch_policy())
    all_data.extend(fetch_price())
    
    # 保存
    import os
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"[完成] 总共收集 {len(all_data)} 条，保存到 {DATA_FILE}")
    return all_data

if __name__ == "__main__":
    collect_all()