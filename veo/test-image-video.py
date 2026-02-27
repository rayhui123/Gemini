import time
from google import genai
from google.genai.types import GenerateVideosConfig, Image, VideoGenerationReferenceImage

client = genai.Client()

# TODO(developer): Update and un-comment below line
# output_gcs_uri = "gs://your-bucket/your-prefix"

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="A person walks in carrying a vase full of flowers and places the vase on a kitchen table.",
    config=GenerateVideosConfig(
        reference_images=[
            VideoGenerationReferenceImage(
                image=Image(
                    gcs_uri="gs://cloud-samples-data/generative-ai/image/vase.png",
                    mime_type="image/png",
                ),
                # 参数解释：reference_type="asset"
                # 这是最关键的设置！它告诉模型将图中的花瓶视为一个固定的“资产”。
                # AI 会在视频运动过程中极力保持这个花瓶的外观不发生畸变或改变。
                reference_type="asset",
            ),
        ],
        aspect_ratio="9:16",
        output_gcs_uri="gs://gemini-ray/output-folder/",
    ),
)

while not operation.done:
    time.sleep(15)
    operation = client.operations.get(operation)
    print(operation)

if operation.response:
    print(operation.result.generated_videos[0].video.uri)

# Example response:
# gs://your-bucket/your-prefix