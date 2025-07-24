from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_models import ChatTongyi
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings
from pydantic import SecretStr
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化通义千问模型和嵌入
llm = ChatTongyi(
    model="qwen-plus",
    api_key=SecretStr(os.getenv("DASHSCOPE_API_KEY") or "")
)
embeddings = DashScopeEmbeddings(
    model="text-embedding-v4",
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
)

# 加载现有的FAISS向量数据库
vectorstore = FAISS.load_local(
    "code/db/watermelon_book_faiss", 
    embeddings,
    allow_dangerous_deserialization=True
)
retriever = vectorstore.as_retriever()

# 创建历史感知检索器
contextualize_q_system_prompt = (
    "给定聊天历史和最新的用户问题，该问题可能引用了聊天历史中的上下文，"
    "请重新组织一个独立的问题，使其能够在没有聊天历史的情况下理解。"
    "不要回答问题，只需在需要时重新组织它，否则按原样返回。"
)
contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

# 创建问答链
system_prompt = (
    "你是一个问答任务的助手。使用以下检索到的上下文来回答问题。"
    "如果你不知道答案，就说你不知道。最多使用三句话，保持答案简洁。"
    "\n\n"
    "{context}"
)
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

# 组合检索链
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# 运行示例
chat_history = []
input_question = "西瓜书的主要内容是什么?"

try:
    result = rag_chain.invoke({
        "input": input_question,
        "chat_history": chat_history
    })
    
    # 更新聊天历史
    chat_history.extend([
        HumanMessage(content=input_question),
        AIMessage(content=result["answer"])
    ])
    
    print("Answer:", result["answer"])
except Exception as e:
    print(f"发生错误: {e}")
    print("这可能是由于向量维度不匹配导致的FAISS索引问题")

