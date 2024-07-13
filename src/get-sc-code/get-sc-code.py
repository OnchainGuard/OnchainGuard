import requests

# Placeholder URLs and API keys for different blockchains
apis = {
    "zcircuit": {
        "url": "https://api.zcircuit.io/api?module=contract&action=getsourcecode&address={address}&apikey={apikey}",
        "apikey": ""
    },
    "scroll": {
        "url": "https://api-sepolia.scrollscan.com/api?module=contract&action=getsourcecode&address={address}&apikey={apikey}",
        "apikey": "XDWU3533W5G2VJYXPHYMGF7U5HE75ZGTHG"
    },
    "arbitrum": {
        "url": "https://api-sepolia.arbiscan.io/api?module=contract&action=getsourcecode&address={address}&apikey={apikey}",
        "apikey": "7C6KFVQMWND5GXM9W69F8YB2VQTAYRJ8EF"
    },
}

def get_contract_code(blockchain, address):
    if blockchain not in apis:
        return f"Blockchain '{blockchain}' is not supported."

    api_info = apis[blockchain]
    url = api_info['url'].format(address=address, apikey=api_info['apikey'])
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == '1' and data['message'] == 'OK':
            return data['result'][0]['SourceCode']
        else:
            return f"Error fetching contract code: {data['result']}"
    else:
        return f"Error: Unable to reach {blockchain} API. Status code: {response.status_code}"

blockchain = 'arbitrum'
contract_address = ''
contract_code = get_contract_code(blockchain, contract_address)
print(contract_code)
