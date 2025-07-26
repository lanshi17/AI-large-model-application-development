"""
数据分析代理程序
该程序使用通义千问大模型和Python REPL工具来分析销售数据。
"""
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from pydantic import SecretStr
import os
import sys
from dotenv import load_dotenv
import pandas as pd
import io

# 加载环境变量
load_dotenv()

# 初始化Python REPL工具用于数据分析
python_repl_tool = PythonREPLTool()
python_repl_tool.name = "python_repl"
python_repl_tool.description = "执行Python代码进行数据分析。输入应该是有效的Python代码。"

# 初始化通义千问大模型
api_key = os.getenv("DASHSCOPE_API_KEY")
if not api_key:
    print("错误：未设置DASHSCOPE_API_KEY环境变量")
    sys.exit(1)

model = ChatOpenAI(
    model="qwen-turbo",
    api_key=SecretStr(api_key) if api_key else None,
    base_url=os.getenv("BASE_URL")
)

# 使用标准的结构化聊天代理提示词模板
prompt = hub.pull("hwchase17/structured-chat-agent")

# 创建结构化聊天代理
agent = create_structured_chat_agent(
    llm=model,
    tools=[python_repl_tool],
    prompt=prompt
)

# 使用AgentExecutor包装代理
agent_executor = AgentExecutor(
    agent=agent,
    tools=[python_repl_tool],
    handle_parsing_errors=True,
    verbose=True
)

# 示例CSV数据
try:
    sample_csv_data = pd.read_csv("code/AI模型工具应用/data.csv")
except FileNotFoundError:
    print("错误：找不到data.csv文件，请确保文件存在于当前目录中")
    sys.exit(1)
except Exception as e:
    print(f"错误：读取data.csv文件时发生错误: {e}")
    sys.exit(1)

if __name__ == "__main__":
    # 先让agent了解数据结构并进行分析
    query = f"""
    我有一个销售数据集，需要你帮我分析。请使用Python代码来处理。
    首先加载数据：
    ```python
    import pandas as pd
    df = pd.read_csv("code/AI模型工具应用/data.csv")
    print("数据形状:", df.shape)
    print("列名:", df.columns.tolist())
    print("前5行数据:")
    print(df.head())然后计算：
    总销售额（quantity * price 的总和）
    找出销售额最高的产品
    请用中文回复分析结果。 """
    
    # 调用代理执行器处理数据分析请求
    result = agent_executor.invoke({
        "input": query
    })
    
    # 打印分析结果
    print("\n=== 结果 ===")
    print(result)