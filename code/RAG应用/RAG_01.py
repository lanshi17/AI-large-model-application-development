# 安装必要的库
# pip install langchain-community openai pydantic ipython python-dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate
from IPython.display import display, display_markdown
from pydantic import SecretStr
from langchain.schema.messages import (SystemMessage, HumanMessage)
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

# 创建聊天模型实例
model=ChatOpenAI(model="qwen-turbo",
                 api_key=SecretStr(os.getenv("DASHSCOPE_API_KEY") or ""),
                 base_url=os.getenv("BASE_URL"),
                 temperature=0.3,
                 frequency_penalty=1.5
                )

# 定义示例提示模板
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "总结以下文档内容:\n{document_content}"),
        ("ai", "##文档摘要\n{summary}")
    ]
)

# 定义示例数据
examples = [
    {
        "document_content": "这是一个示例文档。它包含一些基本信息。",
        "summary": "这是一个包含基本信息的示例文档。"
    },
    {
        "document_content": "这是另一个示例文档。它提供了详细的描述。",
        "summary": "这是一个提供了详细描述的示例文档。"
    }
]

# 定义少样本提示模板
few_shot_template = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

# 定义最终提示模板
final_prompt_template = ChatPromptTemplate.from_messages(
    [
        few_shot_template,
        ("human", "{input}"),
    ]
)

# 加载 PDF 文件
pdf_loader = PyPDFLoader("code/RAG应用/example.pdf")  # 确保 example.pdf 存在于当前目录中
documents = pdf_loader.load_and_split()

# 假设我们只使用第一个文档的内容
document_content = documents[0].page_content

# 生成最终提示
final_prompt = final_prompt_template.invoke(
    {
        "input": f"总结以下文档内容:\n{document_content}"
    }
)
final_prompt.to_messages()

# 调用模型并显示结果
response = model.invoke(
    final_prompt
)
display_markdown(response.content, raw=True)
