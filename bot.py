import json
import time
import cloudscraper
from twocaptcha import TwoCaptcha



site_url = "https://faucet-testnet.singularityfinance.ai/"
site_key = "0x4AAAAAAA2Cr3HyNW-0RONo"


solver = TwoCaptcha(input("Masukkan API Key2Captcha: "))


HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,id;q=0.7",
    "cache-control": "max-age=0",
    "content-type": "application/json",
    "origin": "https://faucet-testnet.singularityfinance.ai",
    "referer": "https://faucet-testnet.singularityfinance.ai/",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}


def solve_captcha():
    print("Bypass captcha...")
    try:
        result = solver.turnstile(sitekey=site_key, url=site_url)
        return result["code"]
    except Exception as e:
        print(f"Error menyelesaikan captcha: {e}")
        return None


def start_session(address, captcha_token):
    url = "https://faucet-testnet.singularityfinance.ai/api/startSession"
    payload = {
        "addr": address,
        "captchaToken": captcha_token,
    }

    scraper = cloudscraper.create_scraper()
    response = scraper.post(url, headers=HEADERS, json=payload)

    if response.status_code == 200:
        data = response.json()
        print(f"Session status: {data['status']}")
        
        if 'session' in data:
            return data["session"]
        else:
            #print("Error: 'session' key not found in response.")
            print(f"Response data: {data}")
            
            
            if data.get('failedCode') == 'RECURRING_LIMIT':
                print("You have reached the session creation limit. Please try again later.")
            return None
    else:
        print(f"Error memulai sesi: {response.text}")
        return None


def claim_reward(session, captcha_token):
    url = "https://faucet-testnet.singularityfinance.ai/api/claimReward"
    payload = {
        "session": session,
        "captchaToken": captcha_token,
    }

    scraper = cloudscraper.create_scraper()
    response = scraper.post(url, headers=HEADERS, json=payload)

    if response.status_code == 200:
        data = response.json()
        print(f"Claim status: {data['status']}")
    else:
        print(f"Error klaim reward: {response.text}")


if __name__ == "__main__":
    address = input("Masukkan Adress: ")

    
    captcha_token = solve_captcha()
    if not captcha_token:
        exit()

    
    session = start_session(address, captcha_token)
    if not session:
        exit()

    
    time.sleep(3)

    
    captcha_token = solve_captcha()
    if not captcha_token:
        exit()

    claim_reward(session, captcha_token)
