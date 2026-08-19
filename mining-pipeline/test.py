import json
from search import search

# 20条测试问题（手写，体现赶工）
TEST_QUERIES = [
    "稀土政策有什么新变化？",
    "铜价最近走势如何？",
    "澳洲锂矿出口政策",
    "稀土出口管制",
    "铜期货价格",
    "矿产资源开发管理办法",
    "稀土行业规范",
    "关键矿产战略",
    "锂矿出口许可",
    "资源税改革",
    "稀土总量控制",
    "铜价高位运行",
    "澳洲关键矿产",
    "稀土环保要求",
    "稀土出口目录",
    "矿产政策调整",
    "铜期货行情",
    "稀土资源税",
    "矿业新闻",
    "价格波动"
]

def evaluate():
    total = len(TEST_QUERIES)
    hit_count = 0
    
    for q in TEST_QUERIES:
        results = search(q, top_k=5)
        if results:
            hit_count += 1
        print(f"Q: {q}")
        print(f"  找到 {len(results)} 条")
        if results:
            print(f"  第一条: {results[0].get('title', '')[:30]}...")
        print()
    
    print(f"===== 评测结果 =====")
    print(f"总查询数: {total}")
    print(f"有结果数: {hit_count}")
    print(f"命中率: {hit_count/total*100:.1f}%")

if __name__ == "__main__":
    evaluate()