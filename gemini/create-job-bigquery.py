import time

from google import genai
from google.genai.types import CreateBatchJobConfig, JobState, HttpOptions

client = genai.Client(http_options=HttpOptions(api_version="v1"))

# TODO(developer): Update and un-comment below line
output_uri = "bq://train-ray-20260104.output_folder.batch_output_01"

job = client.batches.create(
    # To use a tuned model, set the model param to your tuned model using the following format:
    # model="projects/{PROJECT_ID}/locations/{LOCATION}/models/{MODEL_ID}
    model="gemini-2.5-flash",
    src="bq://storage-samples.generative_ai.batch_requests_for_multimodal_input",
    config=CreateBatchJobConfig(dest=output_uri),
)
print(f"Job name: {job.name}")
print(f"Job state: {job.state}")
# Example response:
# Job name: projects/.../locations/.../batchPredictionJobs/9876453210000000000
# Job state: JOB_STATE_PENDING

# See the documentation: https://googleapis.github.io/python-genai/genai.html#genai.types.BatchJob
completed_states = {
    JobState.JOB_STATE_SUCCEEDED,
    JobState.JOB_STATE_FAILED,
    JobState.JOB_STATE_CANCELLED,
    JobState.JOB_STATE_PAUSED,
}

while job.state not in completed_states:
    time.sleep(30)
    job = client.batches.get(name=job.name)
    print(f"Job state: {job.state}")
# Example response:
# Job state: JOB_STATE_PENDING
# Job state: JOB_STATE_RUNNING
# Job state: JOB_STATE_RUNNING
# ...
# Job state: JOB_STATE_SUCCEEDED