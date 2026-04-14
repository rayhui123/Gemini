from google import genai
from IPython.display import display, Image
from google.genai import types

client = genai.Client()

chat = client.chats.create(
   # model="gemini-3-pro-image-preview",
   model="gemini-2.5-flash-image",
   config=types.GenerateContentConfig(
       response_modalities=['TEXT', 'IMAGE']
   )
)

message_1 = "Create an image of a clear perfume bottle sitting on a vanity."
response_1 = chat.send_message(message_1)
data = b''   # 用于存储生成的图片数据，供下一轮使用
for part in response_1.candidates[0].content.parts:
   if part.text:
       print(f"\nAI 回复内容:\n{part.text}")
   if part.inline_data:
       data = part.inline_data.data
       display(Image(data=data, width=500))

# --- 第二轮：基于第一轮的图片进行精确修改 ---
# 只有当第一轮成功生成了数据，我们才进行第二轮
if data:
    print("\n--- 第二轮：进行图像编辑 ---")

    # 构造组合消息：[旧图片数据, 修改指令]
    message_2 = [
       types.Part.from_bytes(
           data=data,
           mime_type="image/png",
       ),
       "Make the perfume bottle purple and add a vase of hydrangeas next to the bottle.",
    ]
    
    response_2 = chat.send_message(message_2)

    for part in response_2.candidates[0].content.parts:
       if part.text:
           print(f"\nAI 回复内容:\n{part.text}")
       if part.inline_data:
           # 更新 data 变量，以便进行可能的第三轮修改
           data = part.inline_data.data 
           display(Image(data=data, width=500))

