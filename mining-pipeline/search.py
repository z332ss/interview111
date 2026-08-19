import json
import re
from collections import Counter

DATA_FILE = "data/news.json"

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def simple_tokenize(text):
    """超简易分词：只保留中文和英文单词"""
    text = text.lower()
    # 中英文混合分词：中文按字符，英文按空格
    words = re.findall(r'[a-zA-Z]+|[一-龥]', text)
    return words

def search(query, top_k=5):
    """关键词匹配检索"""
    data = load_data()
    if not data:
        return []
    
    # 提取用户问题的关键词
    query_words = set(simple_tokenize(query))
    if not query_words:
        return []
    
    # 对每条数据算匹配分
    scores = []
    for item in data:
        # 拼凑文本：标题+内容+来源
        text = f"{item.get('title','')} {item.get('content','')} {item.get('source','')}"
        doc_words = simple_tokenize(text)
        doc_counter = Counter(doc_words)
        
        # 算分：关键词在文档中出现的次数之和
        score = sum(doc_counter.get(w, 0) for w in query_words)
        scores.append((score, item))
    
    # 按分数排序，取top_k
    scores.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scores[:top_k] if _ > 0]