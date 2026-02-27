import time
from google import genai
from google.genai.types import GenerateVideosConfig, Image

client = genai.Client()

# TODO(developer): Update and un-comment below line
# output_gcs_uri = "gs://your-bucket/your-prefix"

operation = client.models.generate_videos(
    model="veo-3.1-generate-001",
    prompt="Extreme close-up of a cluster of vibrant wildflowers swaying gently in a sun-drenched meadow.",
    image=Image(
        gcs_uri="gs://cloud-samples-data/generative-ai/image/flowers.png",       #图片在云端存储桶的地址。模型会参考这张花的图片来生成视频
        mime_type="image/png",     #文件的格式
    ),
    config=GenerateVideosConfig(
        aspect_ratio="16:9",
        output_gcs_uri="gs://gemini-ray/output-folder/",
    ),
)

# 异步轮询任务状态
# 因为视频渲染非常耗时，代码不会卡在发起请求的那一步，而是进入这个循环。
while not operation.done:
    time.sleep(15)
    operation = client.operations.get(operation)
    print(operation)

if operation.response:
    print(operation.result.generated_videos[0].video.uri)