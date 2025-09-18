from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
import torch
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)
model_name='/home/ubuntu/Mistral-7B-Instruct-v0.2'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
        model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    trust_remote_code=True,
    quantization_config = bnb_config
    )
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer = tokenizer,
    torch_dtype=torch.bfloat16,
    device_map="auto", max_new_tokens=5
)
hf = HuggingFacePipeline(pipeline=pipe)



from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
import os
prompt_template = '''<s>[INST] just provide 'yes' or 'no' for whether the following commit message is implementing performance optimization or not.
{commit_message} [/INST]</s>'''

prompt = PromptTemplate(
    input_variables=["commit_message"], template=prompt_template
)
llm = LLMChain(llm=hf, prompt=prompt)

out = llm.run("scsi: ufs: add debug counters for recoverable errors during runtime  There is no way to know how many times various UFS errors happened while system is running if we have successfully recovered from those errors. Those failures should be counted and inspected as they might be anomaly behavior of the driver and can impact performance. This change adds support to capture these failures statistics like how many times we have seen errors, and which type of errors.  To reset the counters: echo 1 > /sys/kernel/debug/ufs/err_stats  To print them out: cat /sys/kernel/debug/ufs/err_stats  Note: There is no need to enable them as they are never disabled. This error counters are something that we always would like to have.")

# Write the output to a file
with open('mistral.txt', 'w') as file:
    file.write(output)
