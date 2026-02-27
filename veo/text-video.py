import time     # 导入时间库，用于在等待任务完成时进行休眠
from google import genai          # 导入 Google GenAI SDK
from google.genai.types import GenerateVideosConfig      # 导入视频生成的配置类

client = genai.Client()

# TODO(developer): Update and un-comment below line
# output_gcs_uri = "gs://your-bucket/your-prefix"

operation = client.models.generate_videos(
    model="veo-3.1-generate-001",
    prompt="a cat reading a book",
    config=GenerateVideosConfig(
        aspect_ratio="16:9",
        output_gcs_uri="gs://gemini-ray/output-folder/",          #生成的视频存储在Google cloud上的存储桶中
    ),
)


# 轮询（Polling）任务状态
# 视频生成不是即时的，需要几分钟时间。因此使用 while 循环等待。
# operation.done: 一个布尔值，如果任务完成（成功或失败）则为 True。
while not operation.done:
    time.sleep(15)                   # 每隔 15 秒检查一次，避免过度频繁请求 API
    operation = client.operations.get(operation)            # 重新获取最新的任务详情，异步处理
    print(operation)

if operation.response:
    print(operation.result.generated_videos[0].video.uri)

# Example response:
# gs://your-bucket/your-prefix