import requests
from google import genai
from google.genai.types import (
    GenerateContentConfig,
    HarmBlockThreshold,
    HarmCategory,
    HttpOptions,
    Part,
    SafetySetting,
)
from PIL import Image, ImageColor, ImageDraw
from pydantic import BaseModel

# Helper class to represent a bounding box
# 定义一个辅助类，用来规范 AI 返回的检测框数据
class BoundingBox(BaseModel):
    """
    Represents a bounding box with its 2D coordinates and associated label.

    Attributes:
        box_2d (list[int]): A list of integers representing the 2D coordinates of the bounding box,
                            typically in the format [y_min, x_min, y_max, x_max].
        label (str): A string representing the label or class associated with the object within the bounding box.
    """
    # box_2d 存储坐标：[y_min, x_min, y_max, x_max]，范围是 0-1000（归一化坐标）
    box_2d: list[int]
    # label 存储物体名称，例如 "blue sock"
    label: str

# Helper function to plot bounding boxes on an image
# 定义一个辅助函数，将AI给出的“数字坐标”在图像上绘制检测框
def plot_bounding_boxes(image_uri: str, bounding_boxes: list[BoundingBox]) -> None:
    """
    Plots bounding boxes on an image with labels, using PIL and normalized coordinates.

    Args:
        image_uri: The URI of the image file.
        bounding_boxes: A list of BoundingBox objects. Each box's coordinates are in
                        normalized [y_min, x_min, y_max, x_max] format.
    """
    with Image.open(requests.get(image_uri, stream=True, timeout=10).raw) as im:
        width, height = im.size      # 获取图片的原始像素宽高
        draw = ImageDraw.Draw(im)   # 创建画笔工具
        
        # 获取内置的所有颜色名称列表，用于区分不同的框
        colors = list(ImageColor.colormap.keys())

        for i, bbox in enumerate(bounding_boxes):
            # Scale normalized coordinates to image dimensions
            # 坐标转换：将 0-1000 的归一化坐标还原为实际像素坐标
            # 公式：像素位置 = (归一化值 / 1000) * 图片实际尺寸
            abs_y_min = int(bbox.box_2d[0] / 1000 * height)
            abs_x_min = int(bbox.box_2d[1] / 1000 * width)
            abs_y_max = int(bbox.box_2d[2] / 1000 * height)
            abs_x_max = int(bbox.box_2d[3] / 1000 * width)

            # 轮流选择不同的颜色来绘制不同的框，增加可视区分度
            color = colors[i % len(colors)]

            # Draw the rectangle using the correct (x, y) pairs
            # 绘图：画出矩形框，outline 是边框颜色，width 是粗细
            draw.rectangle(
                ((abs_x_min, abs_y_min), (abs_x_max, abs_y_max)),
                outline=color,
                width=4,
            )

            # 文字：在框的左上角附近标注标签名
            if bbox.label:
                # Position the text at the top-left corner of the box
                draw.text((abs_x_min + 8, abs_y_min + 6), bbox.label, fill=color)

        im.show()

client = genai.Client(http_options=HttpOptions(api_version="v1"))

# 配置 AI 如何思考和回答
config = GenerateContentConfig(
    system_instruction="""
    Return bounding boxes as an array with labels.
    Never return masks. Limit to 25 objects.
    If an object is present multiple times, give each object a unique label
    according to its distinct characteristics (colors, size, position, etc..).
    """,
    temperature=0.5,  # 随机性适中，保证坐标准确度
    # 设置安全级别：仅拦截极高风险内容，允许正常的图像分析结果返回
    safety_settings=[
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=HarmBlockThreshold.BLOCK_ONLY_HIGH,
        ),
    ],
    response_mime_type="application/json",         # 强制要求返回 JSON 格式
    response_schema=list[BoundingBox],              # 强制要求 JSON 符合 BoundingBox 列表格式
)

# 指定要分析的图片链接
image_uri = "https://storage.googleapis.com/generativeai-downloads/images/socks.jpg"

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        Part.from_uri(
            file_uri=image_uri,
            mime_type="image/jpeg",
        ),
        "Output the positions of the socks with a face. Label according to position in the image.",
    ],
    config=config,
)
print(response.text)
# 调用之前定义的函数，将 AI 的解析结果 (response.parsed) 绘制到图上
plot_bounding_boxes(image_uri, response.parsed)