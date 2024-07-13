import openai
import os
import pandas as pd
import time
from dotenv import load_dotenv
import hashlib

# Load environment variables from .env file
load_dotenv()

def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

openai.api_key = os.getenv('OPENAI_API_KEY')

if not openai.api_key:
    print("API key not found. Please check your .env file.")
    exit(1)

audit_reports_path = '/home/kgorna/Documents/ethglobalbrussels/OnchainGuard/src/solidit-scrapping/audit-reports'
smart_contract_path = '/home/kgorna/Documents/ethglobalbrussels/OnchainGuard/src/check-vuln'
smart_contract_file = 'test-vuln.txt'

smart_contract_content = read_text_file(f"{smart_contract_path}/{smart_contract_file}")
if smart_contract_content is None:
    print("Failed to read the smart contract file.")
    exit(1)

vulnerability_files = [f for f in os.listdir(audit_reports_path) if f.endswith('.txt')][:10]
print(f"Found {len(vulnerability_files)} text files in the directory. Analyzing the first 10 reports.")

results = pd.DataFrame(columns=["Report Name", "Response", "Hashed Response"])

def query_openai(vf, messages):
    retry_delay = 0  # Start with a short delay for retry
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
        except openai.error.RateLimitError as e:
            # print(f"Rate limit error for {vf}, retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff
        except openai.error.OpenAIError as e:
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
        response_text = response.choices[0].message['content']
        hashed_response = hashlib.sha256(response_text.encode()).hexdigest()
        new_row = pd.DataFrame({"Report Name": [vf], "Response": [response_text], "Hashed Response": [hashed_response]})
        results = pd.concat([results, new_row], ignore_index=True)
        if response_text.startswith("Yes"):
            print(f"!!! Vulnerability found in link with report nb {vf}: WARNING SENT TO THE USER FRONTEND.\n")
        elif "No" in response_text:
            print(f"No Vulnerability found in link with report {vf}\n")
    else:
        print(f"Failed to get a valid response for {vf} after retries.")

print(results)

