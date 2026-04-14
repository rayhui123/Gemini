from google import genai
from google.genai.types import HttpOptions, Part

# 初始化客户端
# 这里显式指定了 api_version="v1"，确保调用的是稳定版的 API 接口
client = genai.Client(http_options=HttpOptions(api_version="v1"))

# 定义提示词（Prompt）
# 指令要求：对音频文件中的主要观点提供一个“简洁的总结（concise summary）”
prompt = """Provide a concise summary of the main points in the audio file."""

# 调用模型生成内容
response = client.models.generate_content(
    model="gemini-2.5-flash",  # 使用轻量且快速的 Flash 模型，非常适合处理音频摘要任务
    contents=[
        prompt,  # 输入 1：文字指令
        # 输入 2：音频文件
        # 使用 Part.from_uri 直接指向 Google Cloud Storage 上的音频路径
        Part.from_uri(
            file_uri="gs://cloud-samples-data/generative-ai/audio/pixel.mp3",
            mime_type="audio/mpeg", # 必须指定 MIME 类型，告知模型这是 MP3 格式
        ),
    ],
)

# 打印 AI 听完音频后生成的总结文本
print(response.text)