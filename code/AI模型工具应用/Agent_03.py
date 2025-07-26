from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_experimental.tools import PythonREPLTool
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain import hub
from pydantic import SecretStr
import os
from dotenv import load_dotenv
import pandas as pd
import io

# 加载环境变量
load_dotenv()

# 定义Python代码执行工具输入模型
class PythonCodeInput(BaseModel):
    code: str = Field(description="要执行的Python代码")

# 定义CSV分析工具输入模型
class CSVAnalysisInput(BaseModel):
    csv_content: str = Field(description="CSV文件内容")
    query: str = Field(description="用户查询问题")

# 定义文本计算工具输入模型
class TextCalculationInput(BaseModel):
    expression: str = Field(description="数学表达式")

# 初始化Python REPL工具用于代码执行
python_code_tool = PythonREPLTool()
python_code_tool.name = "python_executor"
python_code_tool.description = "用于执行Python代码的工具，可以进行复杂计算和数据处理"

# 初始化Python REPL工具用于CSV分析
csv_analysis_tool = PythonREPLTool()
csv_analysis_tool.name = "csv_analyzer"
csv_analysis_tool.description = "用于分析CSV数据的工具，可以执行数据统计、计算等操作"

# 初始化Python REPL工具用于文本计算
text_calculation_tool = PythonREPLTool()
text_calculation_tool.name = "text_calculator"
text_calculation_tool.description = "用于计算数学表达式的工具，支持基本和复杂数学运算"

# 初始化通义千问大模型
api_key = os.getenv("DASHSCOPE_API_KEY")
model = ChatOpenAI(
    model="qwen-turbo",
    api_key=SecretStr(api_key) if api_key else None,
    base_url=os.getenv("BASE_URL")
)

# 从Hub拉取结构化聊天代理提示词模板
prompt = hub.pull("hwchase17/structured-chat-agent")

# 创建结构化聊天代理
agent = create_structured_chat_agent(
    llm=model,
    tools=[python_code_tool, csv_analysis_tool, text_calculation_tool],
    prompt=prompt
)

# 使用AgentExecutor包装代理
agent_executor = AgentExecutor(
    agent=agent,
    tools=[python_code_tool, csv_analysis_tool, text_calculation_tool],
    handle_parsing_errors=True,
    verbose=True
)

# 示例CSV数据
sample_csv_data =pd.read_csv("code/AI模型工具应用/data.csv") 
# 示例：运行代理执行器使用不同工具
if __name__ == "__main__":
    # 测试CSV分析工具
    print("=== 测试CSV分析工具 ===")
    result1 = agent_executor.invoke({
        "input": f"""
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
    })
    print(result1)
    
    print("\n=== 测试文本计算工具 ===")
    # 测试文本计算工具
    result2 = agent_executor.invoke({
        "input": "请计算 (150 * 3 + 200) / 5 - 30 的结果"
    })
    print(result2)
    
    print("\n=== 测试Python代码执行工具 ===")
    # 测试Python代码执行工具
    result3 = agent_executor.invoke({
        "input": "请用Python生成一个包含10个随机数的列表，并计算它们的平均值"
    })
    print(result3)
