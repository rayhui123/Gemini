from google import genai
from google.genai.types import Content, FunctionDeclaration, GenerateContentConfig, Part, ThinkingConfig, Tool

client = genai.Client()

# 1. Define your tool
# 这里是在向模型描述你的“技能库”。模型并不直接运行这段代码，而是读取它的描述。
get_weather_declaration = FunctionDeclaration(
   name="get_weather",
   description="Gets the current weather temperature for a given location.",
   parameters={
       "type": "object",
       "properties": {"location": {"type": "string"}},
       "required": ["location"],
   },
)

# 将定义好的函数封装进 Tool 对象，准备传给模型使用
get_weather_tool = Tool(function_declarations=[get_weather_declaration])

# 2. Send a message that triggers the tool
# 2. 发送第一轮消息，触发工具调用
prompt = "What's the weather like in London?"
response = client.models.generate_content(
   model="gemini-2.5-flash",
   contents=prompt,
   config=GenerateContentConfig(
       tools=[get_weather_tool],
       # 核心配置：开启“思考模式”，让模型生成并返回它的推理过程（思考签名）
       thinking_config=ThinkingConfig(include_thoughts=True)
   ),
)

# 3. Handle the function call
# 3. 处理模型生成的函数调用请求
# 模型不会直接回答“天气很好”，而是返回一个 function_call 结构体，告诉你它想调用哪个函数，并提供了参数。
function_call = response.function_calls[0]
location = function_call.args["location"]
print(f"Model wants to call: {function_call.name}")

# Execute your tool (for example, call an API)
# (This is a mock response for the example)
print(f"Calling external tool for: {location}")
function_response_data = {
   "location": location,
   "temperature": "30C",
}

# 4. Send the tool's result back
# Append this turn's messages to history for a final response.
# The `content` object automatically attaches the required thought_signature behind the scenes.
# 4. 将工具执行的结果回传给模型（关键环节！）
# 我们需要构建一个“对话历史”，包含三部分：
# A. 用户的原始问题
# B. 模型刚才生成的“思考签名 + 函数请求” (必须包含，否则模型会丢掉上下文)
# C. 你刚刚查到的工具运行结果
history = [
   Content(role="user", parts=[Part(text=prompt)]),
   # (B) 模型的第一轮响应。这其中包含了至关重要的“思考签名”
   # 就像给模型看它刚才写下的“草稿纸”，它才能接上思路。
   response.candidates[0].content, # Signature preserved here
   # (C) 告诉模型：你要的结果我查到了，这就是数据
   Content(
     role="tool",
     parts=[
         Part.from_function_response(
             name=function_call.name,
             response=function_response_data,
         )
     ],
   )
]

# 5. 第二轮请求：让模型基于“事实数据”整理出最终答案
response_2 = client.models.generate_content(
   model="gemini-2.5-flash",
   contents=history,
   config=GenerateContentConfig(
       tools=[get_weather_tool],
       thinking_config=ThinkingConfig(include_thoughts=True)
   ),
)

# 5. Get the final, natural-language answer
print(f"\nFinal model response: {response_2.text}")