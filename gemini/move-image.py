# 导入 Google GenAI 核心库
from google import genai
# 导入图像处理相关的类型定义：原始参考图、遮罩参考图、遮罩配置、编辑配置
from google.genai.types import (
    Image,
    RawReferenceImage,
    MaskReferenceImage,
    MaskReferenceConfig,
    EditImageConfig,
)

# 初始化客户端（会自动读取你之前设置的 GOOGLE_APPLICATION_CREDENTIALS 环境变量）
client = genai.Client(vertexai=True)

# 定义输出文件路径
output_file = "output-image.png"

# 配置“原始参考图”：告诉 AI 基础图片是什么
raw_ref = RawReferenceImage(
    # 加载本地的图片文件
    reference_image=Image.from_file(location="D:/Gemini/test_resources/fruit.png"),
    reference_id=0, # 给这张图一个编号
)

# 配置“遮罩参考图”：告诉 AI 哪个位置需要被修改
mask_ref = MaskReferenceImage(
    reference_id=1,
    # 加载对应的遮罩图（通常黑白图，白色代表要修改的区域）
    reference_image=Image.from_file(location="D:/Gemini/test_resources/fruit_mask.png"),
    config=MaskReferenceConfig(
        # 模式：使用用户提供的遮罩图
        mask_mode="MASK_MODE_USER_PROVIDED",
        # 遮罩扩张：稍微扩大遮罩边缘，让修改处与原图融合更自然
        mask_dilation=0.01,
    ),
)

# 调用模型进行图像编辑
image = client.models.edit_image(
    model="imagen-3.0-capability-001", # 使用 Imagen 3.0 模型
    prompt="",                         # 提示词为空，配合下面的模式表示“移除”
    reference_images=[raw_ref, mask_ref], # 传入原图和遮罩
    config=EditImageConfig(
        # 编辑模式：INPAINT_REMOVAL（局部消除）
        # 结合空 prompt，AI 会尝试抹除遮罩区域并根据背景自动填充
        edit_mode="EDIT_MODE_INPAINT_REMOVAL",
    ),
)

# 保存生成的图片
image.generated_images[0].image.save(output_file)

# 打印生成结果的大小
print(f"Created output image using {len(image.generated_images[0].image.image_bytes)} bytes")