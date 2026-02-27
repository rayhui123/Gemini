from google import genai
from google.genai.types import HttpOptions

#初始化客户端
#http_options参数：设置底层网络请求
#api_version：指定使用的API版本（v1）
client = genai.Client(http_options=HttpOptions(api_version="v1"))

#调用模型生成内容
#model参数：指定调用的模型名称
#contents参数：输入给AI的提示词（Prompt）
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How does AI work?",
)
print(response.text)
# Example response:
# Okay, let's break down how AI works. It's a broad field, so I'll focus on the ...
#
# Here's a simplified overview:
# ...