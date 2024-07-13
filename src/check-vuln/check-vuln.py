
import openai
import os
import pandas as pd
import time

def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

openai.api_key = 'sk-proj-FSGgvSLdIEszVzvNChc7T3BlbkFJuNvnoIDj6jEYzdzTEXk1'

audit_reports_path = '/home/kgorna/Documents/ethglobalbrussels/OnchainGuard/src/solidit-scrapping/audit-reports'
smart_contract_path = '/home/kgorna/Documents/ethglobalbrussels/OnchainGuard/src/check-vuln'
smart_contract_file = 'test-vuln.txt'

smart_contract_content = read_text_file(f"{smart_contract_path}/{smart_contract_file}")
if smart_contract_content is None:
    print("Failed to read the smart contract file.")
    exit(1)

# List TXT files in the directory and limit to the first 5
vulnerability_files = [f for f in os.listdir(audit_reports_path) if f.endswith('.txt')][:5]
print(f"Found {len(vulnerability_files)} text files in the directory. Analyzing the first 5 reports.")

results = pd.DataFrame(columns=["Report Name", "Response"])

def query_openai(vf, messages):
    retry_delay = 1  # Start with a 10 second delay for retry
    max_retries = 5  # Maximum number of retries
    attempts = 0
    while attempts < max_retries:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-0613",
                messages=messages,
                max_tokens=100,
                temperature=0.7)
            return response
        except openai.error.RateLimitError as e:  # Correct exception class
            print(f"Rate limit error for {vf}, retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff
        except openai.error.OpenAIError as e:  # General OpenAI errors
            print(f"Unhandled OpenAI error for {vf}: {e}")
            return None
        attempts += 1
    return None

for vf in vulnerability_files:
    vulnerability_content = read_text_file(f"{audit_reports_path}/{vf}")
    if vulnerability_content is None:
        continue

    messages = [
        {"role": "system", "content": "You are an expert in security in Solidity. Answer briefly."},
        {"role": "user", "content": f"After reading the following vulnerability report, tell if there's a vulnerability in the smart contract file. If it is no, just answer 'No'. If it is yes, give more details.\n\nVulnerability Report:\n{vulnerability_content}\n\nSmart Contract File:\n{smart_contract_content}"}
    ]

    response = query_openai(vf, messages)
    if response:
        new_row = pd.DataFrame({"Report Name": [vf], "Response": [response.choices[0].message['content']]})
        results = pd.concat([results, new_row], ignore_index=True)
    else:
        print(f"Failed to get a valid response for {vf} after retries.")

print(results)
