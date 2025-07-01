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

  ## 小样本示例模版化
  
  * 示例
  
    ```python
    #gg%%
    import os
    from langchain_openai import ChatOpenAI
    from langchain.prompts import FewShotChatMessagePromptTemplate,ChatPromptTemplate
    from IPython.display import display,display_markdown
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
    # 定义example_prompt
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "格式化以下客户信息:\n姓名 -> {customer_name}\n年龄 -> {customer_age}\n城市 -> {customer_city}"),
            ("ai", "##客户信息\n- 客户姓名: {formatted_name}\n- 客户年龄: {formatted_age}\n- 客户所在地: {formatted_city}")
        ]
    )
    
    
    
    # %%
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
    
    
    # %%
    # 定义few_shot_template
    few_shot_template = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )
    
    # %%
    final_prompt_template=ChatPromptTemplate.from_messages(
        [
            few_shot_template,
            ("human","{input}"),
        ]
    )
    
    # %%
    final_prompt=final_prompt_template.invoke(
        {
            "input":"格式化以下客户信息:\n姓名 -> 刘六\n年龄 -> 28\n城市 -> 南通"
        }
    )
    final_prompt.to_messages()
    
    # %%
    response=model.invoke(
        final_prompt
    )
    display_markdown(response.content,raw=True)
    ```
  
    