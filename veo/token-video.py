from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
  model="gemini-3-pro-preview",
  contents=[
      types.Part(
          file_data=types.FileData(
              file_uri="gs://cloud-samples-data/generative-ai/image/a-man-and-a-dog.png",
              mime_type="image/jpeg",
          ),
          media_resolution=types.PartMediaResolution(
              level=types.PartMediaResolutionLevel.MEDIA_RESOLUTION_HIGH
          ),
      ),
      types.Part(
          file_data=types.FileData(
              file_uri="gs://cloud-samples-data/generative-ai/video/behind_the_scenes_pixel.mp4",
              mime_type="video/mp4",
          ),
          media_resolution=types.PartMediaResolution(
              level=types.PartMediaResolutionLevel.MEDIA_RESOLUTION_LOW
          ),
      ),
      "When does the image appear in the video? What is the context?",     #这张图片什么时候出现在视频中？当时的背景/上下文是什么？
  ],
)
print(response.text)