from google import genai
from google.genai.types import GenerateContentConfig, HttpOptions, Part

# 初始化客户端，指定 API 版本为 v1
client = genai.Client(http_options=HttpOptions(api_version="v1"))

# 定义复杂的转录指令（Prompt）
# 要求：按 [时间码, 发言人, 字幕] 的格式转录，并用 A、B 等代号区分不同说话人
prompt = """Transcribe the interview, in the format of timecode, speaker, caption.
Use speaker A, speaker B, etc. to identify speakers."""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        prompt,
        Part.from_uri(
            file_uri="gs://cloud-samples-data/generative-ai/audio/pixel.mp3",
            mime_type="audio/mpeg",
        ),
    ],
    # 【核心配置】开启音频时间戳功能
    # 必须设置 audio_timestamp=True，模型才会去精确对齐音频的秒数
    config=GenerateContentConfig(audio_timestamp=True),
)

# 打印转录结果
print(response.text)