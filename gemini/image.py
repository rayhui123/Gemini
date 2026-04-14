from google import genai      #导入Google GenAI核心库
from google.genai.types import GenerateContentConfig, Modality
from PIL import Image       #处理和保存图片
from io import BytesIO      #用于在内存中处理二进制数据

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=("Generate an image of the Eiffel tower with fireworks in the background."),
    config=GenerateContentConfig(
        response_modalities=[Modality.TEXT, Modality.IMAGE],
        #核心参数response_modalities：设置AI的回复中既包含文字（TEXT），也包含生成的图片（IMAGE）
    ),
)

#遍历响应结果
for part in response.candidates[0].content.parts:
    if part.text:
        print(part.text)
    elif part.inline_data:
        image = Image.open(BytesIO((part.inline_data.data)))     #将二进制数据转换为PIL图片对象
        image.save("eiffel.png")     #将生成的图片保存到本地