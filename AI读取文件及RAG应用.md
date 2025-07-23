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
- TextLoader example
    ```python
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

    ```

## 文本向量化--嵌入向量
- OpenAIEmbeddings 示例
    ```python
    from langchain_openai import OpenAIEmbeddings
    from langchain_core.pydantic_v1 import SecretStr
    import os
    from dotenv import load_dotenv

    # 加载环境变量
    load_dotenv()

    # 初始化百炼大模型text-embedding-v4
    embeddings = OpenAIEmbeddings(
        model="text-embedding-v4",
        api_key=SecretStr(os.getenv("DASHSCOPE_API_KEY") or ""),
        base_url="https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding-v4"
    )

    # 示例文本
    texts = [
        "这是一个示例文本。",
        "这是另一个示例文本，用于生成嵌入向量。"
    ]

    # 生成嵌入向量
    try:
        embedding_vectors = embeddings.embed_documents(texts)
        print(f"成功生成 {len(embedding_vectors)} 个嵌入向量，每个向量维度为 {len(embedding_vectors[0])}")
    except Exception as e:
        print(f"生成嵌入向量时出错: {e}")

    # 为单个文本生成嵌入向量
    single_text = "这是单个文本示例。"
    try:
        single_embedding = embeddings.embed_query(single_text)
        print(f"单个文本嵌入向量维度: {len(single_embedding)}")
    except Exception as e:
        print(f"生成单个文本嵌入向量时出错: {e}")

    ```
## 向量数据库

通过向量距离进行搜索匹配
 - FAISS 向量数据库示例
    ```python
    import os
    import faiss
    import numpy as np
    from dotenv import load_dotenv
    from langchain_community.embeddings import DashScopeEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain_core.documents import Document

    # 加载环境变量
    load_dotenv()

    # 初始化DashScope嵌入模型
    embeddings = DashScopeEmbeddings(
        model="text-embedding-v4",
        dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
    )

    # 创建示例文档
    documents = [
        Document(page_content="风急天高猿啸哀，渚清沙白鸟飞回。"),
        Document(page_content="无边落木萧萧下，不尽长江滚滚来。"),
        Document(page_content="万里悲秋常作客，百年多病独登台。"),
        Document(page_content="艰难苦恨繁霜鬓，潦倒新停浊酒杯。")
    ]

    # 创建FAISS向量数据库
    try:
        vector_store = FAISS.from_documents(
            documents=documents,
            embedding=embeddings
        )
        print("FAISS向量数据库创建成功")
    except Exception as e:
        print(f"创建FAISS向量数据库时出错: {e}")

    # 保存向量数据库到本地
    try:
        vector_store.save_local("faiss_index")
        print("向量数据库已保存到本地")
    except Exception as e:
        print(f"保存向量数据库时出错: {e}")

    # 从本地加载向量数据库
    try:
        loaded_vector_store = FAISS.load_local(
            folder_path="faiss_index",
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        )
        print("向量数据库加载成功")
    except Exception as e:
        print(f"加载向量数据库时出错: {e}")

    # 执行相似性搜索
    query = "描述秋天景象的诗句"
    try:
        # 生成查询嵌入向量
        query_embedding = embeddings.embed_query(query)
        
        # 使用FAISS进行相似性搜索
        docs = loaded_vector_store.similarity_search(query, k=2)
        print(f"\n与'{query}'相关的文档:")
        for i, doc in enumerate(docs, 1):
            print(f"{i}. {doc.page_content}")
            
        # 也可以使用自定义嵌入向量进行搜索
        docs_by_vector = loaded_vector_store.similarity_search_by_vector(query_embedding, k=2)
        print(f"\n通过向量搜索到的文档:")
        for i, doc in enumerate(docs_by_vector, 1):
            print(f"{i}. {doc.page_content}")
            
    except Exception as e:
        print(f"执行相似性搜索时出错: {e}")

    # 获取向量数据库的FAISS索引对象，可用于更底层的操作
    try:
        faiss_index = loaded_vector_store.index
        print(f"\nFAISS索引信息:")
        print(f"索引类型: {type(faiss_index)}")
        print(f"向量维度: {faiss_index.d}")
        print(f"向量数量: {faiss_index.ntotal}")
    except Exception as e:
        print(f"获取FAISS索引信息时出错: {e}")

    ```

## 自动化RAG对话链

## 不同类型的嵌入向量

