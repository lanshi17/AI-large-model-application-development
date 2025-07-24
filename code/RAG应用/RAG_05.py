from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import PyPDFLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# # 自定义批处理函数来控制API调用批次大小
# def embed_documents_in_batches(embeddings, texts, batch_size=8):
#     """分批处理文档嵌入以避免API限制"""
#     all_embeddings = []
#     for i in range(0, len(texts), batch_size):
#         batch = texts[i:i+batch_size]
#         print(f"正在处理批次 {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1} (大小: {len(batch)})")
#         try:
#             batch_embeddings = embeddings.embed_documents(batch)
#             all_embeddings.extend(batch_embeddings)
#         except Exception as e:
#             print(f"处理批次 {i//batch_size + 1} 时出错: {e}")
#             # 如果批次太大，尝试更小的批次
#             if "batch size is invalid" in str(e) and len(batch) > 1:
#                 print("尝试减半批次大小...")
#                 half_size = len(batch) // 2
#                 for j in range(0, len(batch), half_size):
#                     sub_batch = batch[j:j+half_size]
#                     sub_embeddings = embeddings.embed_documents(sub_batch)
#                     all_embeddings.extend(sub_embeddings)
#             else:
#                 raise e
#     return all_embeddings

 # 初始化嵌入模型
embeddings = DashScopeEmbeddings(
     model="text-embedding-v4",
     dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)

# # 加载OCR处理后的PDF
# pdf_path = "./西瓜书_ocr.pdf"

# def load_scanned_pdf(pdf_path):
#     """加载扫描版PDF"""
#     pages = []
#     try:
#         print("使用PyMuPDFLoader加载OCR后的PDF...")
#         loader = PyMuPDFLoader(pdf_path)
#         pages = loader.load()
#         print(f"成功加载: {len(pages)} 页")
#         return pages
#     except Exception as e:
#         print(f"加载失败: {e}")
#         # 备用方案
#         try:
#             print("尝试使用PyPDFLoader加载...")
#             loader = PyPDFLoader(pdf_path)
#             pages = loader.load()
#             print(f"PyPDFLoader成功加载: {len(pages)} 页")
#             return pages
#         except Exception as e2:
#             print(f"PyPDFLoader也失败: {e2}")
#     return pages

# # 加载PDF文档
# pages = load_scanned_pdf(pdf_path)

# # 检查加载结果
# if not pages:
#     print("未能加载任何页面内容")
# else:
#     print(f"总共加载了 {len(pages)} 页")
#     # 显示前几页的内容统计
#     for i, page in enumerate(pages[:3]):
#         content_length = len(page.page_content)
#         print(f"第{i+1}页内容长度: {content_length} 字符")
#         if content_length > 0:
#             preview = page.page_content[:100].replace('\n', ' ')
#             print(f"  内容预览: {preview}...")

# # 创建文本分割器，调整参数适应中文内容
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=500,      # 减小块大小
#     chunk_overlap=50,    # 重叠减少
#     separators=["\n\n", "\n", "。", "！", "？", "；", "，", ".", " ", ""]
# )

# # 分割文档
# split_docs = []
# if pages:
#     # 过滤掉内容过少的页面
#     filtered_pages = [page for page in pages if len(page.page_content.strip()) > 30]
#     print(f"过滤后有效页面数: {len(filtered_pages)}")
    
#     if filtered_pages:
#         # 分批处理避免内存问题
#         split_docs = text_splitter.split_documents(filtered_pages)
#         print(f"文档分割完成，共 {len(split_docs)} 个片段")
        
#         # 显示分割结果统计
#         if split_docs:
#             lengths = [len(doc.page_content) for doc in split_docs]
#             print(f"片段长度统计 - 最小: {min(lengths)}, 最大: {max(lengths)}, 平均: {sum(lengths)//len(lengths)}")
#             print("前3个分割片段预览:")
#             for i, doc in enumerate(split_docs[:3]):
#                 page_num = doc.metadata.get('page', '未知')
#                 content_preview = doc.page_content[:150].replace('\n', ' ')
#                 print(f"  片段 {i+1} (页码: {page_num}): {content_preview}...")
#     else:
#         print("警告: 没有找到包含足够文本的页面")

# # 为文档片段添加唯一标识
# for i, doc in enumerate(split_docs):
#     doc.metadata["chunk_id"] = i

# # 手动分批创建FAISS向量数据库以避免API限制
# vector_store = None
# if split_docs:
#     try:
#         print("开始创建FAISS向量数据库...")
#         print(f"文档总数: {len(split_docs)}")
        
#         # 提取文本和元数据
#         texts = [doc.page_content for doc in split_docs]
#         metadatas = [doc.metadata for doc in split_docs]
        
#         # 分批获取嵌入向量，每批最多8个避免API限制
#         print("开始获取文档嵌入向量...")
#         document_embeddings = embed_documents_in_batches(embeddings, texts, batch_size=8)
#         print(f"成功获取 {len(document_embeddings)} 个嵌入向量")
        
#         # 创建FAISS向量数据库
#         print("正在构建FAISS索引...")
#         vector_store = FAISS.from_embeddings(
#             text_embeddings=list(zip(texts, document_embeddings)),
#             embedding=embeddings,
#             metadatas=metadatas
#         )
#         print("FAISS向量数据库创建成功")
        
#     except Exception as e:
#         print(f"创建FAISS向量数据库时出错: {e}")
#         import traceback
#         traceback.print_exc()
#         vector_store = None
# else:
#     print("没有文档可供创建向量数据库")

# # 保存向量数据库到本地
# if vector_store:
#     try:
#         vector_store.save_local("./code/db/watermelon_book_faiss")
#         print("向量数据库已保存到本地")
#     except Exception as e:
#         print(f"保存向量数据库时出错: {e}")

# 从本地加载向量数据库
if os.path.exists("./code/db/watermelon_book_faiss/index.faiss"):
    try:
        loaded_vector_store = FAISS.load_local(
            folder_path="./code/db/watermelon_book_faiss",
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        )
        print("向量数据库加载成功")
    except Exception as e:
        print(f"加载向量数据库时出错: {e}")
        loaded_vector_store = None
else:
    print("本地不存在向量数据库文件")
    #loaded_vector_store = vector_store

# 执行相似性搜索示例
if loaded_vector_store:
    queries = [
        "机器学习的定义是什么？",
        "什么是监督学习？",
        "支持向量机的原理",
        "决策树算法"
    ]
    
    for query in queries:
        try:
            docs = loaded_vector_store.similarity_search(query, k=3)
            print(f"\n查询: {query}")
            print("检索结果:")
            for i, doc in enumerate(docs, 1):
                page_num = doc.metadata.get('page', '未知')
                chunk_id = doc.metadata.get('chunk_id', '未知')
                content = doc.page_content[:200].replace('\n', ' ')
                print(f"  {i}. [第{page_num}页, 片段{chunk_id}]: {content}...")
        except Exception as e:
            print(f"查询 '{query}' 时出错: {e}")

    # 使用MMR搜索获取更多样化的结果
    try:
        mmr_docs = loaded_vector_store.max_marginal_relevance_search(
            "机器学习基础概念", 
            k=3, 
            fetch_k=10
        )
        print(f"\nMMR查询: 机器学习基础概念")
        print("MMR检索结果:")
        for i, doc in enumerate(mmr_docs, 1):
            page_num = doc.metadata.get('page', '未知')
            chunk_id = doc.metadata.get('chunk_id', '未知')
            content = doc.page_content[:200].replace('\n', ' ')
            print(f"  {i}. [第{page_num}页, 片段{chunk_id}]: {content}...")
    except Exception as e:
        print(f"执行MMR搜索时出错: {e}")
else:
    print("无法执行搜索，因为没有可用的向量数据库")
