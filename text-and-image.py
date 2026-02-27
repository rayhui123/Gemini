from google import genai
from google.genai.types import GenerateContentConfig, Modality
from PIL import Image
from io import BytesIO

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=(
        "Generate an illustrated recipe for a paella."     #要求生成一份配图的海鲜饭食谱
        "Create images to go alongside the text as you generate the recipe"    #明确要求在文字生成过程中伴随生成图片
    ),
    #配置返回模态：允许同时包含文本和图像
    config=GenerateContentConfig(response_modalities=[Modality.TEXT, Modality.IMAGE]),
)

#将结果保存为Markdown格式，并位于output_folder目录下
with open("output_folder/paella-recipe.md", "w") as fp:

    #遍历返回结果中的每一个“Part”
    for i, part in enumerate(response.candidates[0].content.parts):
        if part.text is not None:
            fp.write(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
            image.save(f"output_folder/example-image-{i+1}.png")   #为图片生成唯一的文件名并保存
            fp.write(f"![image](example-image-{i+1}.png)")