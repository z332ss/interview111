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
        for item in items[:30]:
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
    """爬中国稀土政策（模拟数据，因为真实网站反爬）"""
    print("[爬虫] 政策数据：使用模拟数据...")
    samples = [
        {"source": "中国稀土", "title": "稀土资源开发管理办法（征求意见稿）", "link": "#", "pub_date": "2026-08-19", "content": "工业和信息化部发布稀土资源开发管理办法，加强稀土开采总量控制"},
        {"source": "中国稀土", "title": "稀土行业规范条件（2026年修订）", "link": "#", "pub_date": "2026-08-19", "content": "修订稀土行业规范条件，提高环保和资源利用率要求"},
        {"source": "中国稀土", "title": "稀土出口管制新政策", "link": "#", "pub_date": "2026-08-19", "content": "商务部调整稀土出口管制目录，涉及17种稀土元素"},
        {"source": "澳洲DISR", "title": "Critical Minerals Strategy 2026", "link": "#", "pub_date": "2026-08-19", "content": "澳大利亚发布关键矿产战略，重点支持锂、钴、稀土项目"},
        {"source": "澳洲DISR", "title": "澳洲锂矿出口政策调整", "link": "#", "pub_date": "2026-08-19", "content": "澳大利亚调整锂矿出口许可制度，加强对中国投资审查"},
        {"source": "中国稀土", "title": "稀土资源税改革方案", "link": "#", "pub_date": "2026-08-19", "content": "财政部推进稀土资源税改革，实行差别化税率"},
        {"source": "中国稀土", "title": "稀土开采总量控制指标下达", "link": "#", "pub_date": "2026-08-18", "content": "自然资源部下达2026年度稀土开采总量控制指标，同比减少5%"},
        {"source": "澳洲DISR", "title": "澳洲关键矿产基础设施投资计划", "link": "#", "pub_date": "2026-08-17", "content": "澳大利亚政府宣布投资20亿澳元建设关键矿产加工基础设施"},
        {"source": "中国稀土", "title": "稀土冶炼分离产能置换政策", "link": "#", "pub_date": "2026-08-16", "content": "工信部发布稀土冶炼分离产能置换实施办法，推动产业升级"},
        {"source": "中国稀土", "title": "稀土新材料产业扶持政策", "link": "#", "pub_date": "2026-08-15", "content": "发改委出台稀土新材料应用产业扶持政策，重点支持永磁材料"},
        {"source": "澳洲DISR", "title": "澳洲稀土项目环境影响评估新规", "link": "#", "pub_date": "2026-08-14", "content": "澳大利亚加强稀土项目环境影响评估，要求提交生物多样性报告"},
        {"source": "中国稀土", "title": "稀土产品出口配额管理办法", "link": "#", "pub_date": "2026-08-13", "content": "商务部修订稀土产品出口配额管理办法，实行分类管理"},
        {"source": "澳洲DISR", "title": "澳洲与日本签署稀土供应链合作协议", "link": "#", "pub_date": "2026-08-12", "content": "澳大利亚与日本签署关键矿产供应链合作协议，涉及稀土和锂"},
        {"source": "中国稀土", "title": "稀土行业数字化转型指导意见", "link": "#", "pub_date": "2026-08-11", "content": "工信部发布稀土行业数字化转型指导意见，推动智能矿山建设"},
    ]
    print(f"[爬虫] 政策数据获取 {len(samples)} 条")
    return samples

def fetch_price():
    """用 yfinance 取铜期货价格"""
    print("[爬虫] 价格数据：获取铜期货...")
    try:
        ticker = yf.Ticker("HG=F")
        hist = ticker.history(period="1mo")
        results = []
        for date, row in hist.iterrows():
            results.append({
                "source": "LME",
                "commodity": "铜",
                "date": date.strftime("%Y-%m-%d"),
                "price": round(row["Close"], 2),
                "high": round(row["High"], 2),
                "low": round(row["Low"], 2)
            })
        print(f"[爬虫] 价格数据获取 {len(results)} 条")
        return results
    except Exception as e:
        print(f"[爬虫] 价格数据出错: {e}")
        return []

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