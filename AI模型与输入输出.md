# AI模型与输入输出

## 基本使用方法

- 示例

  ```python
  import os
  from langchain_openai import ChatOpenAI
  from IPython.display import display, Markdown
  from pydantic import SecretStr
  from langchain.schema.messages import SystemMessage, HumanMessage
  from dotenv import load_dotenv
  
  # 加载 .env 文件以获取环境变量
  load_dotenv()
  
  # 初始化 ChatOpenAI 模型，使用从环境变量中获取的 API 密钥和其他参数
  model = ChatOpenAI(
      model="qwen-turbo",
      api_key=SecretStr(os.getenv("DASHSCOPE_API_KEY")),
      base_url=os.getenv("BASE_URL"),
      temperature=0.3,
      frequency_penalty=1.5
  )
  
  # 定义对话消息列表，包含系统消息和人类消息
  messages = [
      SystemMessage(content="请你作为我的物理课助教,用通俗易懂的语言解释物理概念.使用markdown形式"),
      HumanMessage(content="什么是波粒二象性?")
  ]
  
  # 使用模型对对话消息列表进行处理，并获取响应
  response = model.invoke(messages)
  
  # 使用 Markdown 格式显示响应内容
  display(Markdown(response.content))
  ```
  
  

## 模板化输入

- 示例

  ```python
  import os
  from langchain_openai import ChatOpenAI
  from langchain.prompts import SystemMessagePromptTemplate, AIMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
  from IPython.display import display, display_markdown
  from pydantic import SecretStr
  from dotenv import load_dotenv
  
  # 加载 .env 文件以获取环境变量
  load_dotenv()
  
  # 定义系统消息模板，用于设置翻译任务和语言风格
  system_template_text = "你是一位专业翻译者,能够将{input_language}翻译成{output_language},并且输出文本会根据用户要求的任何语言风格进行调整.请只输出翻译后的文本,不要输出额外内容."
  system_prompt_template = SystemMessagePromptTemplate.from_template(system_template_text)
  
  # 显示系统消息模板及其输入变量
  display(system_prompt_template)
  display(system_prompt_template.input_variables)
  
  # 定义人类消息模板，用于提供需要翻译的文本和语言风格
  human_template_text = "文本:{text}\n语言风格:{style}"
  human_prompt_template = HumanMessagePromptTemplate.from_template(human_template_text)
  
  # 使用系统消息模板生成具体的系统消息，指定输入和输出语言
  system_prompt = system_prompt_template.format(input_language="英语", output_language="汉语")
  
  # 使用人类消息模板生成具体的人类消息，指定需要翻译的文本和语言风格
  human_prompt = human_prompt_template.format(text="I'm miss you !", style="诗词")
  
  # 初始化 ChatOpenAI 模型，使用从环境变量中获取的 API 密钥和其他参数
  model = ChatOpenAI(
      model="qwen-turbo",
      api_key=SecretStr(os.getenv("DASHSCOPE_API_KEY")),
      base_url=os.getenv("BASE_URL"),
      temperature=0.3,
      frequency_penalty=1.5
  )
  
  # 使用模型对生成的系统消息和人类消息进行处理，并获取响应
  response = model.invoke([
      system_prompt,
      human_prompt
  ])
  display_markdown(response.content, raw=True)
  
  # 创建一个聊天提示模板，结合系统消息和人类消息模板
  prompt_template = ChatPromptTemplate.from_messages(
      [
          ("system", f"{system_prompt_template.prompt.template}"),
          ("human", f"{human_prompt_template.prompt.template}")
      ]
  )
  
  # 使用聊天提示模板生成具体的提示值，指定输入和输出语言、文本以及语言风格
  prompt_value = prompt_template.invoke(
      {
          "input_language": "English",
          "output_language": "汉语",
          "text": "I'm do love you",
          "style": "诗词"
      }
  )
  
  # 使用模型对生成的提示值进行处理，并获取响应
  response = model.invoke(prompt_value)
  display_markdown(response.content, raw=True)
  
  ```
  

## 小样本示例模版化

- 示例

  ```python
  import os
  from langchain_openai import ChatOpenAI
  from langchain.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate
  from IPython.display import display, display_markdown
  from pydantic import SecretStr
  from langchain.schema.messages import SystemMessage, HumanMessage
  from dotenv import load_dotenv
  
  # 加载 .env 文件以获取环境变量
  load_dotenv()
  
  # 初始化 ChatOpenAI 模型，使用从环境变量中获取的 API 密钥和其他参数
  model = ChatOpenAI(
      model="qwen-turbo",
      api_key=SecretStr(os.getenv("DASHSCOPE_API_KEY")),
      base_url=os.getenv("BASE_URL"),
      temperature=0.3,
      frequency_penalty=1.5
  )
  
  # 定义示例提示模板，用于展示如何格式化客户信息
  example_prompt = ChatPromptTemplate.from_messages(
      [
          ("human", "格式化以下客户信息:\n姓名 -> {customer_name}\n年龄 -> {customer_age}\n城市 -> {customer_city}"),
          ("ai", "##客户信息\n- 客户姓名: {formatted_name}\n- 客户年龄: {formatted_age}\n- 客户所在地: {formatted_city}")
      ]
  )
  
  # 定义一些示例数据，展示如何应用格式化规则
  examples = [
      {
          "customer_name": "张三",
          "customer_age": "27",
          "customer_city": "长沙",
          "formatted_name": "张三",
          "formatted_age": "27岁",
          "formatted_city": "湖南省长沙市"
      },
      {
          "customer_name": "李四",
          "customer_age": "42",
          "customer_city": "广州",
          "formatted_name": "李四",
          "formatted_age": "42岁",
          "formatted_city": "广东省广州市"
      },
      {
          "customer_name": "王五",
          "customer_age": "35",
          "customer_city": "长沙",
          "formatted_name": "王五",
          "formatted_age": "35岁",
          "formatted_city": "湖南省长沙市"
      }
  ]
  
  # 使用示例提示和数据创建一个 FewShotChatMessagePromptTemplate 对象
  few_shot_template = FewShotChatMessagePromptTemplate(
      example_prompt=example_prompt,
      examples=examples,
  )
  
  # 创建最终的提示模板，结合 FewShot 模板和用户输入
  final_prompt_template = ChatPromptTemplate.from_messages(
      [
          few_shot_template,
          ("human", "{input}"),
      ]
  )
  
  # 使用最终的提示模板生成具体的提示，输入为需要格式化的客户信息
  final_prompt = final_prompt_template.invoke(
      {
          "input": "格式化以下客户信息:\n姓名 -> 刘六\n年龄 -> 28\n城市 -> 南通"
      }
  )
  final_prompt.to_messages()
  
  # 使用预设的模型对生成的提示进行处理，并获取响应
  response = model.invoke(final_prompt)
  display_markdown(response.content, raw=True)
  ```

## 从输出中提取列表

- 示例

  ```python
  import os
  from langchain_openai import ChatOpenAI
  from langchain.prompts import ChatPromptTemplate
  from langchain.output_parsers import CommaSeparatedListOutputParser
  from IPython.display import display, display_markdown
  from pydantic import SecretStr
  from dotenv import load_dotenv
  
  # 加载 .env 文件以获取环境变量
  load_dotenv()
  
  # 初始化 ChatOpenAI 模型，使用从环境变量中获取的 API 密钥和其他参数
  model = ChatOpenAI(
      model="qwen-turbo",
      api_key=SecretStr(os.getenv("DASHSCOPE_API_KEY")),
      base_url=os.getenv("BASE_URL"),
      temperature=0.3,
      frequency_penalty=1.5
  )
  
  # 定义聊天提示模板，包含系统消息和人类消息
  prompt = ChatPromptTemplate.from_messages([
      ("system", "{parser_instructions}"),
      ("human", "列出5个{subject}色系的hex编码")
  ])
  
  # 创建一个逗号分隔的列表输出解析器，并获取格式说明
  output_parser = CommaSeparatedListOutputParser()
  parser_instructions = output_parser.get_format_instructions()
  display(parser_instructions)
  
  # 使用提示模板生成具体的提示，指定主题和格式说明
  final_prompt = prompt.invoke(
      {
          "subject": "莫兰迪",
          "parser_instructions": parser_instructions
      }
  )
  
  # 使用模型对生成的提示进行处理，并获取响应
  response = model.invoke(final_prompt)
  display_markdown(response.content, raw=True)
  
  # 使用输出解析器解析响应内容
  parsed_response = output_parser.invoke(response.content)
  
  # 显示解析后的响应类型
  type(parsed_response)
  ```

  

