from langchain_community.embeddings import DashScopeEmbeddings
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 正确初始化DashScope Embeddings
embeddings = DashScopeEmbeddings(
    model="text-embedding-v4",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)

# 测试文本
texts = [
    "风急天高猿啸哀",
    "渚清沙白鸟飞回",
    "无边落木萧萧下",
    "不尽长江滚滚来"
]

# 生成嵌入向量
try:
    embedding_vectors = embeddings.embed_documents(texts)
    print(f"成功生成 {len(embedding_vectors)} 个嵌入向量")
    for i, vec in enumerate(embedding_vectors):
        print(f"文本 {i+1} 向量维度: {len(vec)}")
except Exception as e:
    print(f"生成嵌入向量时出错: {str(e)}")

# 单个文本测试
single_text = "这是单个文本示例。"
try:
    single_embedding = embeddings.embed_query(single_text)
    print(f"单个文本嵌入向量维度: {len(single_embedding)}")
except Exception as e:
    print(f"生成单个文本嵌入向量时出错: {str(e)}")

