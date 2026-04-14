from google import genai
from google.genai.types import HttpOptions, Part

# 初始化GenAI客户端
client = genai.Client(http_options=HttpOptions(api_version="v1"))
model_id = "gemini-2.5-flash"

# 定义提示语，要求对PDF文档进行总结
prompt = """
You are a highly skilled document summarization specialist.
Your task is to provide a concise executive summary of no more than 300 words.
Please summarize the given document for a general audience.
"""

# 从Google Cloud Storage加载PDF文件，并指定其MIME类型
pdf_file = Part.from_uri(
    file_uri="gs://cloud-samples-data/generative-ai/pdf/1706.03762v7.pdf",
    mime_type="application/pdf",
)

# 调用模型生成内容，传入PDF文件和提示语
response = client.models.generate_content(
    model=model_id,
    contents=[pdf_file, prompt],
)

print(response.text)