from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from pydantic import SecretStr
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()
# 初始化模型
model = ChatOpenAI(
    model="qwen-turbo",
    api_key=SecretStr(os.getenv("DASHSCOPE_API_KEY") or ""),
    base_url=os.getenv("BASE_URL"),
    temperature=0.3,
    frequency_penalty=1.5
)

# 自定义TextLoader示例
loader = TextLoader("example.txt", encoding="utf-8")
documents = loader.load()

# 提取文档内容
document_content = documents[0].page_content if documents else ""

# 构建Prompt模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个擅长总结内容的助手。"),
    ("human", "请总结以下文本内容：\n{content}")
])

# 使用LCEL构建链式调用
chain = (
    RunnableParallel(content=RunnablePassthrough())  # 将输入直接传递给prompt中的{content}
    | prompt
    | model
    | StrOutputParser()
)

# 执行并输出结果
summary = chain.invoke(document_content)
print(summary)
