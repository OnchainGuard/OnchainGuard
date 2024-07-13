import sys
import openai
import os
import pandas as pd
import time
from dotenv import load_dotenv
import hashlib
from web3 import Web3
import json

# Load environment variables from .env file
load_dotenv()

# Blockchain configurations
networks = {
    'zcircuit': {
        'rpc_url': 'https://zircuit1.p2pify.com/',
        'contract_address': '0x404CB427F1406b3fd456910e7036f5db81e9C1C0',
        'abi': json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"Registry__ArrayLengthsMismatch","type":"error"},{"inputs":[],"name":"Registry__EmptyScope","type":"error"},{"inputs":[],"name":"Registry__InvalidScansAmount","type":"error"},{"inputs":[],"name":"Registry__OnlyOperator","type":"error"},{"inputs":[],"name":"Registry__OnlyProtocolAdmin","type":"error"},{"inputs":[],"name":"Registry__TooLittleETH","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"protocolId","type":"bytes32"}],"name":"ProtocolAdded","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"protocolId","type":"bytes32"}],"name":"ProtocolRemoved","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"protocolId","type":"bytes32"},{"indexed":false,"internalType":"bytes32","name":"proof","type":"bytes32"}],"name":"ProtocolScanned","type":"event"},{"inputs":[],"name":"PRICE_PER_CONTRACT_SCAN","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_scopeSize","type":"uint256"},{"internalType":"uint256","name":"_scans","type":"uint256"}],"name":"getPrice","outputs":[{"internalType":"uint256","name":"price","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"protocolId","type":"bytes32"}],"name":"getSubscription","outputs":[{"internalType":"address[]","name":"scope","type":"address[]"},{"internalType":"uint256","name":"scans","type":"uint256"},{"internalType":"address","name":"admin","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"protocolId","type":"bytes32"}],"name":"isSubscribed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"operator","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32[]","name":"_protocolIds","type":"bytes32[]"},{"internalType":"bytes32[]","name":"_proofs","type":"bytes32[]"}],"name":"postScan","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"protocolId","type":"bytes32"}],"name":"protocolMapping","outputs":[{"internalType":"uint256","name":"scans","type":"uint256"},{"internalType":"address","name":"admin","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_protocolId","type":"bytes32"},{"internalType":"address[]","name":"_scope","type":"address[]"},{"internalType":"uint256","name":"_scans","type":"uint256"},{"internalType":"address","name":"_admin","type":"address"}],"name":"registerProtocol","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_protocolId","type":"bytes32"},{"internalType":"address[]","name":"_scope","type":"address[]"},{"internalType":"uint256","name":"_scans","type":"uint256"}],"name":"updateSubscription","outputs":[],"stateMutability":"payable","type":"function"}]'),
    },
    'linea': {
        'rpc_url': 'https://linea-sepolia.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161',
        'contract_address': '0x404CB427F1406b3fd456910e7036f5db81e9C1C0',
        'abi': json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"Registry__ArrayLengthsMismatch","type":"error"},{"inputs":[],"name":"Registry__EmptyScope","type":"error"},{"inputs":[],"name":"Registry__InvalidScansAmount","type":"error"},{"inputs":[],"name":"Registry__OnlyOperator","type":"error"},{"inputs":[],"name":"Registry__OnlyProtocolAdmin","type":"error"},{"inputs":[],"name":"Registry__TooLittleETH","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"protocolId","type":"bytes32"}],"name":"ProtocolAdded","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"protocolId","type":"bytes32"}],"name":"ProtocolRemoved","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"protocolId","type":"bytes32"},{"indexed":false,"internalType":"bytes32","name":"proof","type":"bytes32"}],"name":"ProtocolScanned","type":"event"},{"inputs":[],"name":"PRICE_PER_CONTRACT_SCAN","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_scopeSize","type":"uint256"},{"internalType":"uint256","name":"_scans","type":"uint256"}],"name":"getPrice","outputs":[{"internalType":"uint256","name":"price","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"protocolId","type":"bytes32"}],"name":"getSubscription","outputs":[{"internalType":"address[]","name":"scope","type":"address[]"},{"internalType":"uint256","name":"scans","type":"uint256"},{"internalType":"address","name":"admin","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"protocolId","type":"bytes32"}],"name":"isSubscribed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"operator","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32[]","name":"_protocolIds","type":"bytes32[]"},{"internalType":"bytes32[]","name":"_proofs","type":"bytes32[]"}],"name":"postScan","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"protocolId","type":"bytes32"}],"name":"protocolMapping","outputs":[{"internalType":"uint256","name":"scans","type":"uint256"},{"internalType":"address","name":"admin","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_protocolId","type":"bytes32"},{"internalType":"address[]","name":"_scope","type":"address[]"},{"internalType":"uint256","name":"_scans","type":"uint256"},{"internalType":"address","name":"_admin","type":"address"}],"name":"registerProtocol","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_protocolId","type":"bytes32"},{"internalType":"address[]","name":"_scope","type":"address[]"},{"internalType":"uint256","name":"_scans","type":"uint256"}],"name":"updateSubscription","outputs":[],"stateMutability":"payable","type":"function"}]'),
    },
    'arbitrum': {
        'rpc_url': 'https://public.stackup.sh/api/v1/node/arbitrum-sepolia',
        'contract_address': '0xF295E28A89835416804366998cAA314c345DA77c',
        'abi': json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"Registry__ArrayLengthsMismatch","type":"error"},{"inputs":[],"name":"Registry__EmptyScope","type":"error"},{"inputs":[],"name":"Registry__InvalidScansAmount","type":"error"},{"inputs":[],"name":"Registry__OnlyOperator","type":"error"},{"inputs":[],"name":"Registry__OnlyProtocolAdmin","type":"error"},{"inputs":[],"name":"Registry__TooLittleETH","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"protocolId","type":"bytes32"}],"name":"ProtocolAdded","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"protocolId","type":"bytes32"}],"name":"ProtocolRemoved","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"protocolId","type":"bytes32"},{"indexed":false,"internalType":"bytes32","name":"proof","type":"bytes32"}],"name":"ProtocolScanned","type":"event"},{"inputs":[],"name":"PRICE_PER_CONTRACT_SCAN","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_scopeSize","type":"uint256"},{"internalType":"uint256","name":"_scans","type":"uint256"}],"name":"getPrice","outputs":[{"internalType":"uint256","name":"price","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"protocolId","type":"bytes32"}],"name":"getSubscription","outputs":[{"internalType":"address[]","name":"scope","type":"address[]"},{"internalType":"uint256","name":"scans","type":"uint256"},{"internalType":"address","name":"admin","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"protocolId","type":"bytes32"}],"name":"isSubscribed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"operator","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32[]","name":"_protocolIds","type":"bytes32[]"},{"internalType":"bytes32[]","name":"_proofs","type":"bytes32[]"}],"name":"postScan","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"protocolId","type":"bytes32"}],"name":"protocolMapping","outputs":[{"internalType":"uint256","name":"scans","type":"uint256"},{"internalType":"address","name":"admin","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_protocolId","type":"bytes32"},{"internalType":"address[]","name":"_scope","type":"address[]"},{"internalType":"uint256","name":"_scans","type":"uint256"},{"internalType":"address","name":"_admin","type":"address"}],"name":"registerProtocol","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_protocolId","type":"bytes32"},{"internalType":"address[]","name":"_scope","type":"address[]"},{"internalType":"uint256","name":"_scans","type":"uint256"}],"name":"updateSubscription","outputs":[],"stateMutability":"payable","type":"function"}]'),
    },
    'scroll': {
        'rpc_url': 'https://scroll-sepolia.blockpi.network/v1/rpc/public',
        'contract_address': '0xf295e28a89835416804366998caa314c345da77c',
        'abi': json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"Registry__ArrayLengthsMismatch","type":"error"},{"inputs":[],"name":"Registry__EmptyScope","type":"error"},{"inputs":[],"name":"Registry__InvalidScansAmount","type":"error"},{"inputs":[],"name":"Registry__OnlyOperator","type":"error"},{"inputs":[],"name":"Registry__OnlyProtocolAdmin","type":"error"},{"inputs":[],"name":"Registry__TooLittleETH","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"protocolId","type":"bytes32"}],"name":"ProtocolAdded","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"protocolId","type":"bytes32"}],"name":"ProtocolRemoved","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"protocolId","type":"bytes32"},{"indexed":false,"internalType":"bytes32","name":"proof","type":"bytes32"}],"name":"ProtocolScanned","type":"event"},{"inputs":[],"name":"PRICE_PER_CONTRACT_SCAN","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_scopeSize","type":"uint256"},{"internalType":"uint256","name":"_scans","type":"uint256"}],"name":"getPrice","outputs":[{"internalType":"uint256","name":"price","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"protocolId","type":"bytes32"}],"name":"getSubscription","outputs":[{"internalType":"address[]","name":"scope","type":"address[]"},{"internalType":"uint256","name":"scans","type":"uint256"},{"internalType":"address","name":"admin","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"protocolId","type":"bytes32"}],"name":"isSubscribed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"operator","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32[]","name":"_protocolIds","type":"bytes32[]"},{"internalType":"bytes32[]","name":"_proofs","type":"bytes32[]"}],"name":"postScan","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"protocolId","type":"bytes32"}],"name":"protocolMapping","outputs":[{"internalType":"uint256","name":"scans","type":"uint256"},{"internalType":"address","name":"admin","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_protocolId","type":"bytes32"},{"internalType":"address[]","name":"_scope","type":"address[]"},{"internalType":"uint256","name":"_scans","type":"uint256"},{"internalType":"address","name":"_admin","type":"address"}],"name":"registerProtocol","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_protocolId","type":"bytes32"},{"internalType":"address[]","name":"_scope","type":"address[]"},{"internalType":"uint256","name":"_scans","type":"uint256"}],"name":"updateSubscription","outputs":[],"stateMutability":"payable","type":"function"}]'),
    }
}

# Select network based on command-line argument
if len(sys.argv) < 2:
    print("Usage: python check-vuln.py [network]")
    sys.exit(1)

network = sys.argv[1]
if network not in networks:
    print("Invalid network. Available options: 'zcircuit', 'linea', 'arbitrum', 'scroll'")
    sys.exit(1)

config = networks[network]

# Connect to the Ethereum node
w3 = Web3(Web3.HTTPProvider(config['rpc_url']))

# Set up the contract instance
contract = w3.eth.contract(address=config['contract_address'], abi=config['abi'])

# Account details (make sure to securely handle your private key)
account_address = os.getenv('ETH_ACCOUNT_ADDRESS')
private_key = os.getenv('ETH_PRIVATE_KEY')

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

audit_reports_path = os.getenv('AUDIT_REPORTS_PATH')
smart_contract_path = os.getenv('SMART_CONTRACT_PATH')
smart_contract_file = os.getenv('SMART_CONTRACT_FILE')

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
            print(f"!!! Vulnerability found in link with report nb {vf}:\n WARNING SENT TO THE USER FRONTEND.\n")
        elif "No" in response_text:
            print(f"No Vulnerability found in link with report {vf}\n")
    else:
        print(f"Failed to get a valid response for {vf} after retries.")

print(results)

# Helper function to ensure proper bytes32 encoding
def to_bytes32(value):
    return Web3.to_bytes(text=value)[:32].ljust(32, b'\0')

# Function to push hash to the blockchain
def post_scan_on_chain(final_hash):
    protocol_id = to_bytes32('0xf4e649761bcbc50f23f9a4691d424072583cf1c3ddf9ffa6809f7a91076bfdb1')  # example : keccak256("airdrop")
    hash_bytes32 = to_bytes32(final_hash)
    nonce = w3.eth.get_transaction_count(account_address)
    tx = contract.functions.postScan(
        [protocol_id],  # List of protocol IDs
        [hash_bytes32]  # List of proofs
    ).build_transaction({
        'chainId': w3.eth.chain_id,
        'gas': 2000000,
        'gasPrice': w3.to_wei('10', 'gwei'),
        'nonce': nonce,
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Transaction sent! Hash: {tx_hash.hex()}")

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction receipt: {receipt}")

# Generate final hash of all responses and post to blockchain
all_hashes = ''.join(results['Hashed Response'].tolist())
final_hash = hashlib.sha256(all_hashes.encode()).hexdigest()
print(f"Final hash: {final_hash}")
post_scan_on_chain(final_hash)
