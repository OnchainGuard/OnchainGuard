import openai
import os
import pandas as pd
from transformers import BitsAndBytesConfig, AutoTokenizer, AutoModelForCausalLM
import torch


def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

openai.api_key = 'sk-proj-FSGgvSLdIEszVzvNChc7T3BlbkFJuNvnoIDj6jEYzdzTEXk1'

audit_reports_path = 'C:/Users/0/Desktop/Hackathon/OnchainGuard/src/solidit-scrapping/audit-reports'
smart_contract_path = 'C:/Users/0/Desktop/Hackathon/OnchainGuard/src/check-vuln'
smart_contract_file = 'test-vuln.txt'

smart_contract_content = read_text_file(f"{smart_contract_path}/{smart_contract_file}")
if smart_contract_content is None:
    print("Failed to read the smart contract file.")
    exit(1)

# List TXT files in the directory and limit to the first 5
vulnerability_files = [f for f in os.listdir(audit_reports_path) if f.endswith('.txt')][:5]
print(f"Found {len(vulnerability_files)} text files in the directory. Analyzing the first 5 reports.")

results = pd.DataFrame(columns=["Report Name", "Response"])


def init_model():
    try:
        use_4bit = True
        bnb_4bit_compute_dtype = "float16"
        bnb_4bit_quant_type = "nf4"
        use_double_nested_quant = True
        compute_dtype = getattr(torch, bnb_4bit_compute_dtype)

        # BitsAndBytesConfig 4-bit config
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=use_4bit,
            bnb_4bit_use_double_quant=use_double_nested_quant,
            bnb_4bit_quant_type=bnb_4bit_quant_type,
            bnb_4bit_compute_dtype=compute_dtype,
            load_in_8bit_fp32_cpu_offload=False
        )

        # Load the model without quantization
        tokenizer = AutoTokenizer.from_pretrained("AlfredPros/CodeLlama-7b-Instruct-Solidity")
        model = AutoModelForCausalLM.from_pretrained(
            "AlfredPros/CodeLlama-7b-Instruct-Solidity", 
            quantization_config=bnb_config,
            device_map="auto", 
            offload_folder="C:/Users/0/Desktop/Hackathon/OnchainGuard/offload"
        )
        return tokenizer, model
    except Exception as e:
        print(f"Error initializing the LLM.")
        return None
    

tokenizer, model = init_model()

for vf in vulnerability_files:
    vulnerability_content = read_text_file(f"{audit_reports_path}/{vf}")
    if vulnerability_content is None:
        continue


    prompt = f"""### Instruction:
    You are an expert in security in Solidity. Answer briefly.

    ### Task:
    After reading the following vulnerability report, tell if there's a vulnerability in the smart contract file. If it is no, just answer 'No'. If it is yes, give more details.
    
    Vulnerability Report:
    {vulnerability_content}
    
    Smart Contract File:
    {smart_contract_content}

    ### Solution:
    """

    print("\nPrompt:", prompt)
    print("\n\n\nEOS\n\n\n")

    # Tokenize the input
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True, max_length=8192)
    input_ids = inputs.input_ids.cuda()
    attention_mask = inputs.attention_mask.cuda()
    # Run the model to infer an output
    outputs = model.generate(input_ids=input_ids, attention_mask=attention_mask, max_new_tokens=1024, do_sample=True, top_p=0.9, temperature=0.7, pad_token_id=tokenizer.pad_token_id)


    # Detokenize and display the generated output
    response = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0][len(prompt):]
    print(response)

    new_row = pd.DataFrame({"Report Name": [vf], "Response": [response]})
    results = pd.concat([results, new_row], ignore_index=True)

# Display the results
print(results)