import time
from google import genai
from google.genai.types import GenerateVideosConfig, Image

client = genai.Client()

# TODO(developer): Update and un-comment below line
# output_gcs_uri = "gs://your-bucket/your-prefix"

operation = client.models.generate_videos(
    model="veo-3.1-generate-001",
    prompt="a hand reaches in and places a glass of milk next to the plate of cookies",
    #首帧
    image=Image(
        gcs_uri="gs://cloud-samples-data/generative-ai/image/cookies.png",
        mime_type="image/png",
    ),
    config=GenerateVideosConfig(
        aspect_ratio="16:9",
        #尾帧
        last_frame=Image(
            gcs_uri="gs://cloud-samples-data/generative-ai/image/cookies-milk.png",
            mime_type="image/png",
        ),
        output_gcs_uri="gs://gemini-ray/output-folder/",
    ),
)

while not operation.done:
    time.sleep(15)
    operation = client.operations.get(operation)
    print(operation)

if operation.response:
    print(operation.result.generated_videos[0].video.uri)
