import time
from google import genai
from google.genai.types import CreateBatchJobConfig, JobState, HttpOptions

# 1. 初始化客户端
# 批量推理通常需要 v1 版本的 API 支持
client = genai.Client(http_options=HttpOptions(api_version="v1"))

# 2. 设置输出位置（核心步骤）
# 你需要准备一个 Google Cloud Storage (GCS) 的地址来接收结果文件
# 格式示例: "gs://你的存储桶名字/结果文件夹"
output_uri = "gs://gemini-ray/output-folder/" 

# 3. 创建批量任务
# 
job = client.batches.create(
    # 指定使用的模型。如果要用自己微调过的模型，需要传入完整的项目路径
    model="gemini-2.5-flash",
    
    # 源数据地址 (src): 指向一个包含多条请求的 JSONL 文件
    # 官方示例文件包含了一系列预设的 Prompt
    src="gs://cloud-samples-data/batch/prompt_for_batch_gemini_predict.jsonl",
    
    # 任务配置: 指定结果存放的目标地址 (dest)
    config=CreateBatchJobConfig(dest=output_uri),
)

# 打印任务的基础信息
print(f"任务名称: {job.name}")
print(f"当前状态: {job.state}")
# 初始状态通常是 JOB_STATE_PENDING (排队中)

# 4. 定义任务完成的状态集合
# 只要状态进入这四种之一，就意味着任务已经结束（成功、失败或人为停止）
completed_states = {
    JobState.JOB_STATE_SUCCEEDED, # 成功
    JobState.JOB_STATE_FAILED,    # 失败
    JobState.JOB_STATE_CANCELLED, # 已取消
    JobState.JOB_STATE_PAUSED,    # 已暂停
}

# 5. 轮询（Polling）机制：监控任务进度
# 批量推理是异步的，可能需要几分钟到几小时不等
while job.state not in completed_states:
    print(f"任务正在处理中... 当前状态: {job.state}")
    
    # 每隔 30 秒检查一次，避免频繁刷新 API
    time.sleep(30)
    
    # 刷新任务对象，获取服务器端的最新状态
    job = client.batches.get(name=job.name)

# 最终结果输出
if job.state == JobState.JOB_STATE_SUCCEEDED:
    print("🎉 任务圆满完成！你可以去 GCS 存储桶查看结果文件了。")
else:
    print(f"❌ 任务结束，最终状态为: {job.state}")