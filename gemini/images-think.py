from google import genai
from google.genai.types import HttpOptions, Part

# 初始化客户端。
# HttpOptions(api_version="v1") 显式指定使用 v1 版本的 API。
client = genai.Client(http_options=HttpOptions(api_version="v1"))

# 场景 1：定义存储在 Google Cloud Storage (GCS) 上的图片路径
# 注意：这正是你之前报错的地方，确保 gs:// 后的桶名和路径完全正确。
gcs_file_img_path = "gs://gemini-ray/image/result.png"

# 场景 2：读取本地文件
# 以“二进制读取”(rb) 模式打开本地图片并存入 local_file_img_bytes 变量。
with open("D:\\Gemini\\example-image-NB3.png", "rb") as f:
    local_file_img_bytes = f.read()

# 调用 generate_content 接口
response = client.models.generate_content(
    model="gemini-2.5-flash",  # 请确认你当前的 API 支持 2.5 版本，否则建议改回 1.5-flash
    contents=[
        # 提示词：要求 AI 找出两张图中包含的所有物体
        "Generate a list of all the objects contained in both images.",
        
        # 处理云端图片：使用 Part.from_uri，直接通过 GCS 链接读取
        Part.from_uri(file_uri=gcs_file_img_path, mime_type="image/png"),
        
        # 处理本地图片：使用 Part.from_bytes，将读取到的二进制数据传给 AI
        Part.from_bytes(data=local_file_img_bytes, mime_type="image/png"),
    ],
)

# 打印 AI 返回的文字描述
print(response.text)