import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_FILE = "data/news.json"

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

# 全局变量
_vectorizer = None
_vectors = None
_data = None

def build_index():
    global _vectorizer, _vectors, _data
    if _vectors is not None:
        return
    
    _data = load_data()
    if not _data:
        print("[向量库] 没有数据")
        return
    
    texts = [f"{item.get('title','')} {item.get('content','')} {item.get('source','')}" for item in _data]
    # 使用字符级 n-gram，保留单字词
    _vectorizer = TfidfVectorizer(max_features=500, analyzer='char', ngram_range=(1, 2))
    _vectors = _vectorizer.fit_transform(texts)
    print(f"[向量库] 索引构建完成，共 {len(_data)} 条数据，维度: {_vectors.shape}")

def search(query, top_k=5):
    build_index()
    if _vectorizer is None or _vectors is None or _data is None:
        print("[向量库] 索引未构建")
        return []
    
    query_vec = _vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, _vectors).flatten()
    
    top_indices = similarities.argsort()[-top_k:][::-1]
    results = []
    for idx in top_indices:
        if similarities[idx] > 0:
            results.append(_data[idx])
    
    print(f"[查询] '{query}' 找到 {len(results)} 条")
    return results