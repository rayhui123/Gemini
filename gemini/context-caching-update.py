from datetime import datetime as dt
from datetime import timezone as tz
from datetime import timedelta

from google import genai
from google.genai.types import HttpOptions, UpdateCachedContentConfig

# 1. 初始化客户端，使用 v1 正式版接口
client = genai.Client(http_options=HttpOptions(api_version="v1"))

# 2. 指定要操作的缓存名称
# 格式通常为 'projects/{项目编号}/locations/global/cachedContents/{缓存唯一ID}'
cache_name = 'projects/990470530334/locations/global/cachedContents/7702923171342581760'

# 3. 获取缓存详情
# 使用 client.caches.get 方法从服务器拉取该缓存的元数据
content_cache = client.caches.get(name=cache_name)
print("当前过期时间:", content_cache.expire_time)
# 输出示例: 2025-02-20 15:50:18.434482+00:00

# 4. 方式一：使用 TTL（生存时间）更新过期时间
# 将缓存的有效期设置为从“现在”起往后推 36000 秒（即 10 小时）
content_cache = client.caches.update(
    name=cache_name, 
    config=UpdateCachedContentConfig(ttl="36000s")
)

# 计算并打印新的过期时间与当前时间的差值
time_diff = content_cache.expire_time - dt.now(tz.utc)
print("更新后过期时间 (TTL 方式):", content_cache.expire_time)
print("剩余秒数:", time_diff.seconds)
# 预期输出剩余秒数接近 35999

# 5. 方式二：使用特定时间戳（Timestamp）更新过期时间
# 这种方式更精确。这里我们设置为当前时间往后推 7 天
next_week_utc = dt.now(tz.utc) + timedelta(days=7)

# 使用 expireTime 参数直接指定一个具体的 datetime 对象
content_cache = client.caches.update(
    name=cache_name, 
    config=UpdateCachedContentConfig(expireTime=next_week_utc)
)

print("更新后过期时间 (时间戳方式):", content_cache.expire_time)
# 输出示例: 2025-03-16 15:51:42.614968+00:00 (假设今天是3月9日)