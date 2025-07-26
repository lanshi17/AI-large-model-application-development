from langchain_experimental.tools import PythonREPLTool
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain import hub
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, SecretStr
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 定义计算商品总价的工具输入模型
class PriceCalculationInput(BaseModel):
    product_prices: list = Field(description="商品单价列表")
    quantities: list = Field(description="商品数量列表")

# 初始化Python REPL工具，用于执行价格计算
python_repl_tool = PythonREPLTool()
python_repl_tool.name = "price_calculator"
python_repl_tool.description = "用于计算商品总价的工具，接收商品单价和数量列表"

# 初始化通义千问大模型
api_key = os.getenv("DASHSCOPE_API_KEY")
model = ChatOpenAI(
    model="qwen-turbo",
    api_key=SecretStr(api_key) if api_key else None,
    base_url=os.getenv("BASE_URL")
)

# 使用官方的结构化聊天代理提示模板
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

# 示例：运行代理执行器计算商品总价
if __name__ == "__main__":
    result = agent_executor.invoke({
        "input": "我买了3件商品，单价分别是100元、200元和150元，数量分别是2件、1件和3件，请计算总价。"
    })
    print(result)