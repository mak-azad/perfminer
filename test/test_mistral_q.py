from vllm import LLM, SamplingParams

prompts =list(df)
prompt_template='''<s>[INST] Evaluate the commit message provided. If the commit message explicitly indicates the implementation of performance optimization, answer 'Yes'. Otherwise, answer 'No'. The response should strictly be either 'Yes' or 'No' without any additional information or explanation. Do not consider commit messages that do not clearly relate to performance optimization.
Commit_message: {prompt} [/INST] 
Model Answer: </s>
'''

prompts = [prompt_template.format(prompt=prompt) for prompt in prompts]

sampling_params = SamplingParams(temperature=0.01, top_k=1, top_p=0.95,max_tokens=5)

llm = LLM(model="/home/ubuntu/Mixtral-8x7B-Instruct-v0.1-AWQ/", quantization="awq", dtype="auto",tensor_parallel_size=1,gpu_memory_utilization=0.9, enforce_eager=True)

outputs = llm.generate(prompts, sampling_params)

# Print the outputs.
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Generated text: {generated_text}")