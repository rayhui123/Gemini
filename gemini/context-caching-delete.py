from google import genai

client = genai.Client()
# Delete content cache using name
# E.g cache_name = 'projects/111111111111/locations/.../cachedContents/1111111111111111111'
cache_name = 'projects/990470530334/locations/global/cachedContents/7702923171342581760'     # 之前创建的缓存 ID
client.caches.delete(name=cache_name)
print("Deleted Cache", cache_name)
# Example response
#   Deleted Cache projects/111111111111/locations/.../cachedContents/1111111111111111111