import os
from sentence_transformers import SentenceTransformer

# 设置国内镜像
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

print("开始下载模型...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("下载完成！")