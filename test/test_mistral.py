from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
import re
device = "cuda" 

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True, # Enables loading the model in 4-bit precision
    bnb_4bit_quant_type="nf4", # Specifies the quantization type
    bnb_4bit_use_double_quant=True, # Enables double quantization for better precision
)
# Loading the tokenizer
tokenizer = AutoTokenizer.from_pretrained("/home/ubuntu/Mistral-7B-Instruct-v0.2")
# Loading the model with BitsAndBytes configuration, and additional settings from Method-1
model = AutoModelForCausalLM.from_pretrained(
    "/home/ubuntu/Mistral-7B-Instruct-v0.2",
    torch_dtype=torch.float16, # Sets the tensor type to float16 for faster computation
    device_map="auto", # Automatically maps the model layers to the available devices
    trust_remote_code=True, # Allows the execution of remote code for custom model configurations
    #attn_implementation="flash_attention_2", # Uses a specific attention implementation optimized for performance
    quantization_config=bnb_config, # Applies the BitsAndBytes configuration
)


prompt_template = ''' <s> [INST] You are an analytical tool specialized in processing and classifying GitHub Commit message. Your task is to assess developer's intent in a given commit message and categorize it into one of the following predefined categories based on its content:
                      
                      'Yes':  A commit messages that explicitly mentions performance improvement or optimization, specifically in terms of execution time or resource utilization or trade-off between the two. The message should clearly indicate actions that made the code runs faster or  more efficiently, use less memory, or more efficiently utilize system resources. Also, if a commit message describes a change made to address a performance bottleneck, prevent performance degradation, reduce overheads or solve a problem that negatively affects performance. This includes optimizations like replacing inefficient code patterns that are known to kill performance even if the message does not use the words 'improvement' or 'performance' explicitly.
                      'No': A commit message that do not pertain to performance enhancements. This includes messages related to code changes for testing, documentation, performance profiling/monitoring/debugging/analysis and bug/error/crash fixes that don't explicitly mention performance improvement of the application itself, code refactoring or feature addition without explicit performance optimization,  and mentions of necessary or speculative or potential performance enhancements without concrete evidence or results. Also, a messages that is irrelevant, unclear, or ambiguous, and those that do not provide enough context to determine their intent.     

                    If the commit message doesn't fit clearly into any of the above categories, classify it as: 'No'. Additionally, pay close attention to the context in which terms like 'performance', 'improve' or 'improvements' are used. Not all improvements are related to performance—only, classify a message as 'Yes' if it specifically mentions enhancements related to execution time, memory usage, or resource efficiency. Avoid making assumptions based on ambiguous terms. You should have high confidence in classifying a message as 'Yes' based on careful examination of the information provided in the commit message.
                    If you encounter a commit message with multiple intentions, where at least one of those intentions includes a performance improvement in terms of execution time or resource utilization., classify the entire message as 'Yes'.
                    You will only respond with the predefined category. Do not include the word 'Category'. Do not provide explanations or notes.
                    
                    Commit message : ```{commit_message}``` [/INST] Model answer:  </s> '''


sample_commit_message = "the patch improves the run time at the expense of using more ram in some situations. please note: it doesn't improve the actual algorithm (iteration over all permutations). thanks to alexei sheplyakov."
generated_prompt = prompt_template.format(commit_message=sample_commit_message)

inputs = tokenizer.apply_chat_template(
            [{'role': 'user', 'content': generated_prompt}],
            return_tensors="pt"
        ).to(model.device)

outputs = model.generate(
        inputs, 
        max_new_tokens=5,
        do_sample=False)

def parse_output(out):
    res = re.search(r'\b(Yes|No)\b', out)
    if res:
        return res.group(0)
    else:
        return None

value = parse_output(tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True))
if value == 'Yes':
    print("Perf")
else:
    print("NonPerf")
    print(tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True))