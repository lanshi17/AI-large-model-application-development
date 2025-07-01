# AI模型与输入输出

## 基本使用方法

- 示例

  ```python
  # %%
  import os
  from langchain_openai import ChatOpenAI
  from IPython.display import display, Markdown, Image
  from pydantic import SecretStr
  from langchain.schema.messages import (SystemMessage,HumanMessage)
  from dotenv import load_dotenv
  # 加载 .env 文件
  load_dotenv()
  
  # %%
  model=ChatOpenAI(model="qwen-turbo",
                   api_key=SecretStr(os.getenv("DASHSCOPE_API_KEY")),
                   base_url=os.getenv("BASE_URL"),
                   temperature=0.3,
                   frequency_penalty=1.5
                  )
  
  
  # %%
  messages=[
      SystemMessage(content="请你作为我的物理课助教,用通俗易懂的语言解释物理概念.使用markdown形式"),
      HumanMessage(content="什么是波粒二象性?"),
  ]
  
  response=model.invoke(messages)
  display(Markdown(response.content))
  ```

  

## 模板化输入

- 示例

  ```python
  # %%
  import os
  from langchain_openai import ChatOpenAI
  from langchain.prompts import SystemMessagePromptTemplate,AIMessagePromptTemplate,HumanMessagePromptTemplate,ChatPromptTemplate
  from IPython.display import display,display_markdown
  from pydantic import SecretStr
  from langchain.schema.messages import (SystemMessage,HumanMessage)
  from dotenv import load_dotenv
  # 加载 .env 文件
  load_dotenv()
  
  # %%
  system_template_text="你是一位专业翻译者,能够将{input_language}翻译成{output_language},并且输出文本会根据用户要求的任何语言风格进行调整.请只输出翻译后的文本,不要输出额外内容."
  
  system_prompt_template=SystemMessagePromptTemplate.from_template(system_template_text)
  
  display(system_prompt_template)
  display(system_prompt_template.input_variables)
  
  # %%
  human_template_text="文本:{text}\n语言风格:{style}"
  
  human_prompt_template=HumanMessagePromptTemplate.from_template(human_template_text)
  
  # %%
  system_prompt = system_prompt_template.format(input_language="英语",output_language="汉语")
  
  human_prompt=human_prompt_template.format(text="I'm miss you !",style="诗词")
  
  # %%
  model=ChatOpenAI(model="qwen-turbo",
                   api_key=SecretStr(os.getenv("DASHSCOPE_API_KEY")),
                   base_url=os.getenv("BASE_URL"),
                   temperature=0.3,
                   frequency_penalty=1.5
                  )
  
  # %%
  response=model.invoke([
      system_prompt,
      human_prompt
  ])
  display_markdown(response.content,raw=True)
  
  # %%
  prompt_template=ChatPromptTemplate.from_messages(
      [
          ("system",f"{system_prompt_template.prompt.template}"),
          ("human",f"{human_prompt_template.prompt.template}")
      ]
  )
  
  # %%
  prompt_value=prompt_template.invoke(
      {
          "input_language":"English",
          "output_language":"汉语",
          "text":"I'm do love you",
          "style":"诗词"
      }
  )
  
  # %%
  response=model.invoke(prompt_value)
  display_markdown(response.content,raw=True)
  
  ```

  