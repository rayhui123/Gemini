from google import genai
# 导入图像编辑所需的特定配置类型
from google.genai.types import (
    Image,               # 必须导入 Image 类才能使用 from_file
    RawReferenceImage,
    MaskReferenceImage,
    MaskReferenceConfig,
    EditImageConfig,
)

# 初始化客户端（如果是 Vertex AI 环境，建议使用 genai.Client(vertexai=True)）
client = genai.Client()

# 设置输出结果的文件名
output_file = r"D:\Google Cloud SDK\output_folder\output-image.png"

# 配置“原始参考图”：这是你要处理的底图
raw_ref = RawReferenceImage(
    reference_image=Image.from_file(location="D:/Gemini/test_resources/fruit_mask.png"),
    reference_id=0,
)

# 配置“遮罩参考图”：注意这里发生了变化！
mask_ref = MaskReferenceImage(
    reference_id=1,
    reference_image=None,  # 重要：这里不需要提供遮罩文件，因为我们要让 AI 自动识别
    config=MaskReferenceConfig(
        # 核心设置：告诉 AI 自动定位并遮住“前景”物体（例如图片中的水果）
        mask_mode="MASK_MODE_FOREGROUND",
    ),
)

# 调用 Imagen 3.0 模型进行编辑
image = client.models.edit_image(
    model="imagen-3.0-capability-001",
    prompt="",  # 提示词为空，配合 REMOVAL 模式，AI 会用背景填充被抹去的区域
    reference_images=[raw_ref, mask_ref],
    config=EditImageConfig(
        # 编辑模式：局部消除并填充 (Inpaint Removal)
        edit_mode="EDIT_MODE_INPAINT_REMOVAL",
    ),
)

# 保存生成的图像到本地
image.generated_images[0].image.save(output_file)

# 打印生成成功后的文件大小信息
print(f"Created output image using {len(image.generated_images[0].image.image_bytes)} bytes")