from google import genai
from google.genai.types import HttpOptions, Part

client = genai.Client(http_options=HttpOptions(api_version="v1"))
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        Part.from_uri(
            file_uri="gs://gemini-ray/veo/test04.mp4",
            mime_type="video/mp4",
        ),
        "What is in the video?",
    ],
)
print(response.text)