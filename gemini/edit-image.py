from google import genai
from google.genai.types import GenerateContentConfig, Modality
from PIL import Image
from io import BytesIO

client = genai.Client()

# Using an image of Eiffel tower, with fireworks in the background.
#参数：Image.open()会将磁盘上的图片加载为Python中的Image对象
image = Image.open(r"D:\Gemini\output_folder\example-image-eiffel-tower.png")

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[image, "Edit this image to make it look like a cartoon."],
    config=GenerateContentConfig(response_modalities=[Modality.TEXT, Modality.IMAGE]),
)
for part in response.candidates[0].content.parts:
    if part.text:
        print(part.text)
    elif part.inline_data:
        image = Image.open(BytesIO((part.inline_data.data)))       # BytesIO 用于将内存中的字节流模拟成一个文件对象，供 Image.open 读取
        image.save("output_folder/bw-example-image.png")