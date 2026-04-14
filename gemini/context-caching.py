from google import genai
from google.genai.types import Content, CreateCachedContentConfig, HttpOptions, Part

# 1. 初始化客户端
# api_version="v1" 指定使用正式版接口，确保缓存功能调用稳定
client = genai.Client(http_options=HttpOptions(api_version="v1"))

# 2. 定义系统指令 (System Instruction)
# 这一部分会被永久缓存，确保 AI 始终以“事实研究员”的身份处理数据
system_instruction = """You are an expert researcher. You always stick to the facts in the sources provided, and never make up new facts.Now look at these research papers, and answer the following questions."""

# 3. 准备需要缓存的大规模数据 (PDF 论文)
# 这里的 PDF 文件存储在 Google Cloud Storage (gs://) 中
contents = [
    Content(
        role="user",    # 角色可以是 "user" 或 "system"，这里我们用 "user" 来表示这是用户提供的内容
        parts=[
            # 第一篇论文：可能是关于 Gemini 模型的原始论文
            Part.from_uri(
                file_uri="gs://cloud-samples-data/generative-ai/pdf/2312.11805v3.pdf",
                mime_type="application/pdf",
            ),
            # 第二篇论文：可能是关于长上下文理解的研究
            Part.from_uri(
                file_uri="gs://cloud-samples-data/generative-ai/pdf/2403.05530.pdf",
                mime_type="application/pdf",
            ),
        ],
    )
]

# 4. 创建上下文缓存 (Content Cache)
# 这一步会将上述 PDF 数据预处理并存储在云端
content_cache = client.caches.create(
    model="gemini-2.5-flash", # 指定支持缓存的模型版本
    config=CreateCachedContentConfig(
        contents=contents,             # 缓存的主体内容
        system_instruction=system_instruction, # 缓存的系统提示词
        
        # display_name: 给缓存起个名字，方便在控制台查看
        display_name="example-cache",
        
        # ttl (Time To Live): 缓存有效期。
        # "86400s" 表示 24 小时。超时后缓存会自动删除以节省存储费用。
        ttl="86400s",
    ),
)

# 5. 输出结果
# 打印缓存的名称（格式通常为 'cachedContents/xxxxxx'），这个 ID 是后续对话的关键
print(f"缓存 ID: {content_cache.name}")

# 打印使用元数据，包括缓存了多少个 Token
# 你可以通过这个数据计算出你节省了多少首词延迟（TTFT）
print(f"使用统计: {content_cache.usage_metadata}")