from langchain.chains import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
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
    model="qwen-max",  
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

# 1. Stuff方法 - 直接将所有文档传递给LLM
stuff_system_prompt = (
    "你是一个问答任务的助手。使用以下检索到的上下文来回答问题。"
    "如果你不知道答案，就说你不知道。最多使用三句话，保持答案简洁。"
    "\n\n"
    "{context}"
)
stuff_qa_prompt = ChatPromptTemplate.from_messages([
    ("system", stuff_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])
stuff_chain = create_stuff_documents_chain(llm, stuff_qa_prompt)

# 2. Map-Reduce方法 - 将文档分块处理然后汇总
# Map步骤提示词
map_template = """以下是一些文档片段:
{docs}
请根据这些文档回答以下问题:
{question}
答案:"""
map_prompt = PromptTemplate.from_template(map_template)

# Reduce步骤提示词
reduce_template = """以下是一组文档摘要:
{docs}
请根据这些摘要回答原始问题:
{question}
最终答案:"""
reduce_prompt = PromptTemplate.from_template(reduce_template)

# 创建Map-Reduce链（使用LCEL）
def process_documents_map_reduce(input_dict):
    """
    处理Map-Reduce逻辑
    
    Args:
        input_dict (dict): 包含输入问题和上下文文档的字典
            - "input": 用户的查询问题
            - "context": 检索到的相关文档列表
    
    Returns:
        dict: 包含最终答案的字典，格式为 {"answer": final_answer}
    """
    question = input_dict["input"]
    docs = input_dict["context"]
    
    # Map阶段：为每个文档生成摘要
    map_chain = map_prompt | llm | StrOutputParser()
    summaries = []
    for doc in docs:
        summary = map_chain.invoke({
            "docs": doc.page_content,
            "question": question
        })
        summaries.append(summary)
    
    # Reduce阶段：整合所有摘要
    reduce_chain = reduce_prompt | llm | StrOutputParser()
    final_answer = reduce_chain.invoke({
        "docs": "\n\n".join(summaries),
        "question": question
    })
    
    return {"answer": final_answer}

def format_input_for_map_reduce(input_dict):
    """
    格式化输入以适配Map-Reduce链
    
    Args:
        input_dict (dict): 原始输入字典
        
    Returns:
        dict: 格式化后的字典，包含input和context字段
    """
    return {
        "input": input_dict["input"],
        "context": input_dict["context"]
    }

map_reduce_chain = RunnableLambda(format_input_for_map_reduce) | RunnableLambda(process_documents_map_reduce)

# 3. Refine方法 - 迭代式优化答案
def refine_documents(input_dict):
    """
    Refine方法实现，通过迭代方式逐步优化答案
    
    Args:
        input_dict (dict): 包含输入问题和上下文文档的字典
            - "input": 用户的查询问题
            - "context": 检索到的相关文档列表
    
    Returns:
        dict: 包含最终答案的字典，格式为 {"answer": current_answer}
    """
    question = input_dict["input"]
    docs = input_dict["context"]
    
    # 初始答案
    initial_response = llm.invoke(question)
    initial_answer = initial_response.content if hasattr(initial_response, 'content') else str(initial_response)
    
    # 迭代优化
    refine_prompt_template = PromptTemplate.from_template(
        "原始问题: {question}\n已提供的答案: {existing_answer}\n"
        "现在你有机会通过以下更多上下文来改进答案(仅在需要时)。\n"
        "------------\n{context_str}\n------------\n"
        "根据新的上下文，改进原始答案。如果你不能改进答案，只需返回原始答案。"
    )
    
    current_answer = initial_answer
    for doc in docs:
        refine_chain = refine_prompt_template | llm | StrOutputParser()
        current_answer = refine_chain.invoke({
            "question": question,
            "existing_answer": current_answer,
            "context_str": doc.page_content
        })
    
    return {"answer": current_answer}

refine_chain = RunnableLambda(refine_documents)

# 4. Map-Rerank方法 - 对文档进行重新排序
def map_rerank_documents(input_dict):
    """
    Map-Rerank方法实现，为每个文档生成答案并评分，返回最高分的答案
    
    Args:
        input_dict (dict): 包含输入问题和上下文文档的字典
            - "input": 用户的查询问题
            - "context": 检索到的相关文档列表
    
    Returns:
        dict: 包含最终答案的字典，格式为 {"answer": answer}
    """
    question = input_dict["input"]
    docs = input_dict["context"]
    
    # 为每个文档生成答案并打分
    rerank_prompt_template = PromptTemplate.from_template(
        "请根据以下文档回答问题，并为答案的相关性打分(0-100):\n"
        "问题: {question}\n"
        "文档: {context}\n"
        "格式化答案如下:\n"
        "分数: [分数]\n"
        "答案: [答案]"
    )
    
    rerank_chain = rerank_prompt_template | llm | StrOutputParser()
    
    doc_scores = []
    for doc in docs:
        try:
            response = rerank_chain.invoke({
                "question": question,
                "context": doc.page_content
            })
            
            # 解析响应中的分数和答案
            lines = response.split('\n')
            score_line = None
            answer_line = None
            
            for line in lines:
                if line.startswith("分数:"):
                    score_line = line
                elif line.startswith("答案:"):
                    answer_line = line
                    
            if score_line and answer_line:
                score = int(score_line.split(":")[1].strip())
                answer = answer_line.split(":")[1].strip()
                doc_scores.append((score, answer))
            else:
                # 如果格式不正确，给默认低分
                doc_scores.append((0, response))
        except Exception:
            # 如果解析失败，给默认低分
            doc_scores.append((0, "无法解析答案"))
    
    # 按分数排序，返回最高分的答案
    doc_scores.sort(key=lambda x: x[0], reverse=True)
    
    if doc_scores and doc_scores[0][0] > 0:
        return {"answer": doc_scores[0][1]}  # 返回最高分的答案
    else:
        return {"answer": "无法生成相关答案"}

rerank_chain = RunnableLambda(map_rerank_documents)

# 创建不同的检索链
stuff_rag_chain = create_retrieval_chain(history_aware_retriever, stuff_chain)

# 为其他方法创建完整的检索链
# 使用RunnableParallel并行处理输入，然后传递给map_reduce_chain
map_reduce_rag_chain = (
    RunnableParallel({
        "input": lambda x: x["input"],
        "context": history_aware_retriever,
        "chat_history": lambda x: x["chat_history"]
    })
    | map_reduce_chain
)

# 使用RunnableParallel并行处理输入，然后传递给refine_chain
refine_rag_chain = (
    RunnableParallel({
        "input": lambda x: x["input"],
        "context": history_aware_retriever,
        "chat_history": lambda x: x["chat_history"]
    })
    | refine_chain
)

# 使用RunnableParallel并行处理输入，然后传递给rerank_chain
rerank_rag_chain = (
    RunnableParallel({
        "input": lambda x: x["input"],
        "context": history_aware_retriever,
        "chat_history": lambda x: x["chat_history"]
    })
    | rerank_chain
)

# 运行示例
chat_history = []
input_question = "西瓜书的主要内容是什么?"

print("=== 使用Stuff方法 ===")
try:
    result = stuff_rag_chain.invoke({
        "input": input_question,
        "chat_history": chat_history
    })
    print("Answer:", result["answer"])
except Exception as e:
    print(f"Stuff方法出错: {e}")

print("\n=== 使用Map-Reduce方法 ===")
try:
    result = map_reduce_rag_chain.invoke({
        "input": input_question,
        "chat_history": chat_history
    })
    print("Answer:", result["answer"])
except Exception as e:
    print(f"Map-Reduce方法出错: {e}")

print("\n=== 使用Refine方法 ===")
try:
    result = refine_rag_chain.invoke({
        "input": input_question,
        "chat_history": chat_history
    })
    print("Answer:", result["answer"])
except Exception as e:
    print(f"Refine方法出错: {e}")

print("\n=== 使用Map-Rerank方法 ===")
try:
    result = rerank_rag_chain.invoke({
        "input": input_question,
        "chat_history": chat_history
    })
    print("Answer:", result["answer"])
except Exception as e:
    print(f"Map-Rerank方法出错: {e}")