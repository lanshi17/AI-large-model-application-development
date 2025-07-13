# AI读取文件及RAG应用

## 如何让AI知道私人数据--RAG

- 准备外部数据

- 用户提问后搜索

- 询问模型

  ![Screenshot_2025-07-13-11-02-35-62_8f8b568ee7d700593e57db955accad2e.jpg](https://free.picui.cn/free/2025/07/13/6873225158442.jpg)

## 外部文档读取

- TXT加载示例

  ```python
  import os
  from langchain_community.document_loaders import TextLoader
  from langchain.memory import ConversationBufferMemory
  from langchain.chat_models import ChatOpenAI
  from langchain.chains import ConversationChain
  
  # 设置你的OpenAI API密钥
  os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"
  
  # 加载文本文件
  loader = TextLoader("example.txt")
  documents = loader.load()
  
  # 将文档内容合并成一个字符串
  document_content = "\n".join([doc.page_content for doc in documents])
  
  # 创建一个ConversationBufferMemory实例
  memory = ConversationBufferMemory()
  
  # 初始化ChatOpenAI模型
  chat_model = ChatOpenAI(model_name="gpt-3.5-turbo")
  
  # 创建一个ConversationChain实例
  conversation_chain = ConversationChain(
      llm=chat_model,
      memory=memory,
      verbose=True
  )
  
  # 示例对话
  user_input_1 = f"请阅读以下文本并回答问题：\n{document_content}\n问题：这段文本的第一句话是什么？"
  response_1 = conversation_chain.run(user_input_1)
  print(f"AI: {response_1}")
  
  user_input_2 = "请继续回答：这段文本的第二句话是什么？"
  response_2 = conversation_chain.run(user_input_2)
  print(f"AI: {response_2}")
  
  user_input_3 = "请总结这段文本的主要内容。"
  response_3 = conversation_chain.run(user_input_3)
  print(f"AI: {response_3}")
  
  ```
  
- PDF加载示例

  ```python
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
  model = ChatOpenAI(
      model="gpt-3.5-turbo",
      api_key=SecretStr(os.getenv("OPENAI_API_KEY")),  # 确保使用正确的 API 密钥变量名
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
  pdf_loader = PyPDFLoader("example.pdf")  # 确保 example.pdf 存在于当前目录中
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
  ```

  

- 在线资源加载示例

  ```python
  # 安装必要的库
  # pip install langchain_community openai pydantic ipython
  
  from langchain_community.document_loaders import WikipediaLoader
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
  model = ChatOpenAI(
      model="gpt-3.5-turbo",
      api_key=SecretStr(os.getenv("OPENAI_API_KEY")),  # 确保使用正确的 API 密钥变量名
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
  
  # 加载 Wikipedia 页面
  wikipedia_loader = WikipediaLoader(query="LangChain", lang="zh")
  documents = wikipedia_loader.load()
  
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
  ```

## 文本块应用



## 文本向量化--嵌入向量

## 向量数据库

## 自动化RAG对话链

## 不同类型的嵌入向量

