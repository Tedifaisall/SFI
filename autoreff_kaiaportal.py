from web3 import Web3
from eth_account.messages import encode_defunct
from curl_cffi import requests
import time
import secrets

web3 = Web3()

# Log to a text file
def log(txt):
    with open('datawalletkaiaportal.txt', "a") as f:
        f.write(txt + '\n')

def submitReff(addr, token, codereff, retries=3):
    try:
        url = f"https://api-portal.kaia.io/api/v1/referrals/{codereff}/{addr}"
        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {token}",
            "origin": "https://portal.kaia.io",
            "referer": "https://portal.kaia.io/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        }
        
        for attempt in range(retries):
            try:
                response = requests.put(url, headers=headers, impersonate="safari17_0")
                response_json = response.json()
                
                if response.status_code == 200:
                    return response_json
                else:
                    print(f"Error on attempt {attempt + 1}: {response_json.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"Error on attempt {attempt + 1}: {str(e)}")
                
            # Wait for a short time before retrying
            time.sleep(2)
        
        # If we exhausted all retries and still failed
        return {"error": "Max retries reached, request failed"}
    
    except Exception as e:
        print(str(e))
        
def getAuth(addr, msg, signature, retries=3):
    try:
        url = f"https://api-portal.kaia.io/api/v1/auth/jwt"
        headers = {
            "content-type": "application/json",
            "origin": "https://portal.kaia.io",
            "referer": "https://portal.kaia.io/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        }
        
        data = {
            "address": addr,
            "message": msg,
            "signature": signature
        }
        
        for attempt in range(retries):
            try:
                response = requests.post(url, headers=headers, json=data, impersonate="safari17_0")
                response_json = response.json()
                
                if response.status_code == 200:
                    return response_json
                else:
                    print(f"Error on attempt {attempt + 1}: {response_json.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"Error on attempt {attempt + 1}: {str(e)}")
                
            # Wait for a short time before retrying
            time.sleep(2)
        
        # If we exhausted all retries and still failed
        return {"error": "Max retries reached, request failed"}
    
    except Exception as e:
        print(str(e))
    
def getNonce(addr, retries=3):
    try:
        url = f"https://api-portal.kaia.io/api/v1/auth/nonce/{addr}"
        headers = {
            "content-type": "application/json",
            "origin": "https://portal.kaia.io",
            "referer": "https://portal.kaia.io/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        }
        
        for attempt in range(retries):
            try:
                response = requests.get(url, headers=headers, impersonate="safari17_0")
                response_json = response.json()
                
                if response.status_code == 200:
                    return response_json
                else:
                    print(f"Error on attempt {attempt + 1}: {response_json.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"Error on attempt {attempt + 1}: {str(e)}")
                
            # Wait for a short time before retrying
            time.sleep(2)
        
        # If we exhausted all retries and still failed
        return {"error": "Max retries reached, request failed"}
    
    except Exception as e:
        print(str(e))

# Main execution
codereff = input('Input Your Refferal Code Portal Kaia : ')
totalreff = int(input('Input Total Refferal : '))
def main():
    success_count = 0
    fail_count = 0
    
    try:
        for i in range(totalreff):
            print(f'Processing refferal code {codereff} with total refferal {totalreff}/{i+1}...')
            wallet = web3.eth.account.from_key(secrets.token_hex(32))
            print(f'Processing get nonce for wallet address {wallet.address}...')
            get_nonce = getNonce(wallet.address)
            
            if get_nonce["result"].get("nonce") is None:
                print(f'Get nonce failed!')
                time.sleep(1)
            else:
                print(f'Get nonce success!')        
                msg = (f'Click to sign in and accept the Terms of Service\n'
                       f'This request will not trigger a blockchain transaction or cost any gas fees.\n\n'
                       f'Your authentication status will reset after 24 hours.\n\n'
                       f'Wallet address:\n{wallet.address}\n\n'
                       f'Timestamp:\n{get_nonce["result"]["timestamp"]}\n\n'
                       f'Nonce:\n{get_nonce["result"]["nonce"]}\n\n')
                message = encode_defunct(text=msg)
                signed_message = web3.eth.account.sign_message(message, wallet.key)
                signature = web3.to_hex(signed_message.signature)
                
                print(f'Processing access token for wallet address {wallet.address}...')
                get_auth = getAuth(wallet.address, msg, signature)
                time.sleep(1)
                
                if get_auth["result"].get("access_token") is None:
                    print(f'Get access token failed!')
                    time.sleep(1)
                else:
                    print(f'Get access token success!')
                    print(f'Processing submit refferal code {codereff} for wallet address {wallet.address}...')
                    submit_reff = submitReff(wallet.address, get_auth["result"]["access_token"], codereff)
                    time.sleep(1)
                    
                    if submit_reff["code"] == 200:
                        print(f'Submit refferal code {codereff} for wallet address {wallet.address} success!')
                        log(f'{wallet.address}|{web3.to_hex(wallet.key)}')
                        success_count += 1
                        time.sleep(1)
                    else:
                        print(f'Submit refferal code {codereff} for wallet address {wallet.address} failed!')
                        fail_count += 1
                        time.sleep(1)
        
    except Exception as e:
        print(f'Error: {str(e)}')
    
    print(f'Total Successful Submissions: {success_count}')
    print(f'Total Failed Submissions: {fail_count}')

main()
