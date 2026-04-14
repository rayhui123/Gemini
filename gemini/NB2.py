import os
from google import genai
from PIL import Image
from google.genai.types import GenerateContentConfig, Modality
from io import BytesIO

# 1. 强制在代码层面加载身份文件，无视任何窗口环境变量
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"D:\train-ray-20260104-c7b21f1b7b56.json"

# 2. 显式初始化，把参数直接填在括号里
client = genai.Client(
    vertexai=True,
    project="train-ray-20260104",  # 你的项目 ID
    location="global"        # 你的区域
)


response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=("A cat reading a newspaper"),
    config=GenerateContentConfig(
        response_modalities=[Modality.TEXT, Modality.IMAGE],
    ),
)
for part in response.candidates[0].content.parts:
    if part.text:
        print(part.text)
    elif part.inline_data:
        image = Image.open(BytesIO((part.inline_data.data)))
        image.save("D:\\gemini\\example-image-NB3.png")