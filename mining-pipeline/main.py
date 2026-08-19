from fastapi import FastAPI, Query
from search import search
import uvicorn

app = FastAPI(title="矿业新闻检索API", version="0.1")

@app.get("/query")
def query_news(q: str = Query(..., description="自然语言问题")):
    """检索接口"""
    results = search(q, top_k=5)
    return {
        "query": q,
        "total": len(results),
        "results": results
    }

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)