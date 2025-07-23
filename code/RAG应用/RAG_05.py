from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化嵌入模型
embeddings = DashScopeEmbeddings(
    model="text-embedding-v4",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)

# 创建示例文档集合
documents = [
    Document(page_content="人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。", metadata={"source": "ai_intro"}),
    Document(page_content="机器学习是人工智能的一个子集，它使计算机能够从数据中学习并做出决策或预测，而无需明确编程来执行特定任务。", metadata={"source": "ml_intro"}),
    Document(page_content="深度学习是机器学习的一个分支，它模仿人脑的工作方式来处理数据和创建模式，用于决策制定。", metadata={"source": "dl_intro"}),
    Document(page_content="自然语言处理是人工智能领域中的一个重要方向，它致力于让计算机理解和生成人类语言。", metadata={"source": "nlp_intro"})
]

# 创建文本分割器
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

# 分割文档
split_docs = text_splitter.split_documents(documents)

# 创建FAISS向量数据库
vector_store = FAISS.from_documents(
    documents=split_docs,
    embedding=embeddings
)

# 保存向量数据库到本地
vector_store.save_local("faiss_store")

# 从本地加载向量数据库
loaded_vector_store = FAISS.load_local(
    folder_path="faiss_store",
    embeddings=embeddings,
    allow_dangerous_deserialization=True
)

# 执行相似性搜索
query = "什么是人工智能？"
docs = loaded_vector_store.similarity_search(query, k=3)

print(f"查询: {query}")
print("检索结果:")
for i, doc in enumerate(docs, 1):
    print(f"{i}. {doc.page_content} (来源: {doc.metadata.get('source', 'unknown')})")

# 使用MMR(Maximal Marginal Relevance)搜索
mmr_docs = loaded_vector_store.max_marginal_relevance_search(query, k=3, fetch_k=5)
print("\nMMR检索结果:")
for i, doc in enumerate(mmr_docs, 1):
    print(f"{i}. {doc.page_content} (来源: {doc.metadata.get('source', 'unknown')})")

# 添加新文档到现有向量数据库
new_documents = [
    Document(page_content="计算机视觉是人工智能的一个重要应用领域，它使计算机能够从图像或视频中识别和理解内容。", metadata={"source": "cv_intro"})
]

# 添加文档并保存
loaded_vector_store.add_documents(new_documents)
loaded_vector_store.save_local("faiss_store")

# 验证新增文档
new_query = "计算机视觉是什么？"
new_docs = loaded_vector_store.similarity_search(new_query, k=2)
print(f"\n新增文档后查询: {new_query}")
for i, doc in enumerate(new_docs, 1):
    print(f"{i}. {doc.page_content} (来源: {doc.metadata.get('source', 'unknown')})")

