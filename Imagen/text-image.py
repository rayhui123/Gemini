from google import genai
from google.genai.types import GenerateImagesConfig

# 初始化客户端
# 默认会读取环境变量 GOOGLE_APPLICATION_CREDENTIALS 中的服务账号密钥
client = genai.Client()

# TODO(developer): Update and un-comment below line
output_file = r"D:\Google Cloud SDK\output_folder\result.png"

image = client.models.generate_images(
    model="imagen-4.0-generate-001",
    prompt="A dog reading a newspaper",
    config=GenerateImagesConfig(
        image_size="2K",       #参数image_size：设置生成图片的比例或分辨率
    ),
)

image.generated_images[0].image.save(output_file)

print(f"Created output image using {len(image.generated_images[0].image.image_bytes)} bytes")
# Example response:
# Created output image using 1234567 bytes