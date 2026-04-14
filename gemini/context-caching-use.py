from google import genai
from google.genai.types import GenerateContentConfig, HttpOptions

client = genai.Client(http_options=HttpOptions(api_version="v1"))
# Use content cache to generate text response
cache_name = 'projects/990470530334/locations/global/cachedContents/7702923171342581760'     # 之前创建的缓存 ID
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Summarize the pdfs",     # 总结这些 PDF 文件
    config=GenerateContentConfig(
        cached_content=cache_name,
    ),
)
print(response.text)