import requests
from eth_account import Account
import time
from eth_account.messages import encode_defunct
import random

userAgent = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/122.0.2365.92",
]

def verif_kode_referral(invite_code):
    url = "https://referralapi.layeredge.io/api/referral/verify-referral-code"
    headers = {
        'accept': 'application/json, text/plain, */*',
        #'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,id;q=0.8',
        'content-length': '26',
        'content-type': 'application/json',
        'origin': 'https://dashboard.layeredge.io',
        'priority': 'u=1, i',
        'referer': 'https://dashboard.layeredge.io/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': random.choice(userAgent)
    }
    payload = {"invite_code": invite_code}
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def register_wallet(invite_code, wallet_address):
    url = f"https://referralapi.layeredge.io/api/referral/register-wallet/{invite_code}"
    headers = {
        'accept': 'application/json, text/plain, */*',
        #'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,id;q=0.8',
        'content-length': '62',
        'content-type': 'application/json',
        'origin': 'https://dashboard.layeredge.io',
        'priority': 'u=1, i',
        'referer': 'https://dashboard.layeredge.io/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': random.choice(userAgent)
    }
    payload = {"walletAddress": wallet_address}
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def node_activation(node_address, private_key, timestamp):
    # Create the message to sign
    message = f"Node activation request for {node_address} at {timestamp}"
    
    # Encode the message as a SignableMessage
    encoded_message = encode_defunct(text=message)
    
    # Sign the message
    signed_message = Account.sign_message(encoded_message, private_key)
    sign = signed_message.signature.hex()  # Get the signature in hex format

    url = f"https://referralapi.layeredge.io/api/light-node/node-action/{node_address}/start"
    headers = {
        'accept': 'application/json, text/plain, */*',
        #'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9,id;q=0.8',
        'content-length': '169',
        'content-type': 'application/json',
        'origin': 'https://dashboard.layeredge.io',
        'priority': 'u=1, i',
        'referer': 'https://dashboard.layeredge.io/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': random.choice(userAgent)
    }
    payload = {
        "sign": sign,
        "timestamp": timestamp
    }
    response = requests.post(url, headers=headers, json=payload)
    #print("Response from node_activation API:", response.json())
    return response.json()

def generate_wallet_eth():
    account = Account.create()
    return account.address, account._private_key.hex()  # Return both address and private key

def main():
    print("""
    ==========================================================
     LayerEdge Auto Referral Bot v0.1 - by @TEDI_FAISAL
    ==========================================================
    """)

    invite_code = input("Masukkan kode referral: ")
    iterations = int(input("Mau berapa Refferal: "))
    success_count = 0
    failed_count = 0
    for _ in range(iterations):
        wallet_address, private_key = generate_wallet_eth()  # Get both address and private key
        print(f"\nProgress: {_ + 1}/{iterations}")
        print(f"Wallet address: {wallet_address}")
        response = verif_kode_referral(invite_code)
        
        if response.get("data", {}).get("valid", False):
            print("Kode referral valid")
            register_response = register_wallet(invite_code, wallet_address)
            print(f"Registered wallet address successfully: {register_response['data']['walletAddress']}")
            
            # Node activation
            timestamp = int(time.time() * 1000)  # generate timestamp in milliseconds
            node_activation_response = node_activation(wallet_address, private_key, timestamp)
            print(f"Node {wallet_address} activated successfully at {timestamp}")
            success_count += 1
        else:
            print(f"Kode referral tidak valid, {response.get('message', '')}")
            failed_count += 1
        time.sleep(5)

    print(f"\nTotal success: {success_count}, Total failed: {failed_count}")

if __name__ == "__main__":
    main()
