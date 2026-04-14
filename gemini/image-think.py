from google import genai
from google.genai.types import HttpOptions, Part
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"D:\train-ray-20260104-c7b21f1b7b56.json"

client = genai.Client(
    vertexai=True,
    project="train-ray-20260104",  # 你的项目 ID
    location="global"        # 你的区域
)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        "What is shown in this image?",
        Part.from_uri(
            file_uri="gs://gemini-ray/image/result.png",
            mime_type="image/png",
        ),
    ],
)
print(response.text)