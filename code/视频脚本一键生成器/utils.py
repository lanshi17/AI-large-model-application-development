from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper
import os
from pydantic import SecretStr
from dotenv import load_dotenv
# 加载 .env 文件
load_dotenv()
def generate_script(subject, video_length, creativity, api_key):
    """
    生成视频脚本函数。

    参数:
    subject (str): 视频主题
    video_length (int): 视频时长，单位为分钟
    creativity (float): 创意系数，影响输出内容的创意程度
    api_key (str): API密钥

    返回:
    tuple: 维基百科搜索结果、视频标题、视频脚本
    """
    # 创建标题生成模板和脚本生成模板
    title_template = ChatPromptTemplate.from_messages([
        ("human", "请为'{subject}'这个主题的视频想一个吸引人的标题")
    ])

    script_template = ChatPromptTemplate.from_messages([
        ("human",
         """
         你是一位短视频频道的博主。根据以下标题和相关信息,为短视频频道写一个视频脚本。
        视频标题：{title}，视频时长:{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
        要求开头抓住限球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
        整体内容的表达方式要尽量轻松有趣，吸引年轻人。
        脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
        {wikipedia_search}
        """
        )
    ])
    # 初始化大模型
    model = ChatOpenAI(model="qwen-turbo",
                      api_key=SecretStr(os.getenv("OPENAI_API_KEY")),  # 从环境变量获取API密钥
                      base_url=os.getenv("BASE_URL"),
                      temperature=creativity,
                      frequency_penalty=1.5
                      )
    # 创建标题链和脚本链
    title_chain = title_template | model
    script_chain = script_template | model

    # 生成视频标题
    title = title_chain.invoke({"subject": subject}).content

    # 初始化维基百科搜索工具并搜索相关内容
    search = WikipediaAPIWrapper(lang="zh", wiki_client=None)
    search_result = search.run(subject)

    # 生成视频脚本
    script = script_chain.invoke({
        "title": title,
        "duration": video_length,
        "wikipedia_search": search_result
    }).content

    return search_result, title, script


