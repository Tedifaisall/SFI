import json
import random
import time
from pathlib import Path

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumbase import Driver

site_url = "https://faucet-testnet.singularityfinance.ai/"
site_key = "0x4AAAAAAA2Cr3HyNW-0RONo"

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


class Colors:
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


class Icons:
    SUCCESS = "✓"
    ERROR = "✗"
    INFO = "ℹ"
    WARNING = "⚠"
    PROCESS = "⚙"


def solve_captcha():
    print(f"{Colors.YELLOW}{Icons.INFO} Getting captcha token...{Colors.RESET}")
    try:
        driver = Driver(uc=True, headless=True)

        try:
            driver.uc_open_with_reconnect(site_url, reconnect_time=7)

            time.sleep(7)

            token_element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.NAME, "cf-turnstile-response"))
            )

            token = token_element.get_attribute("value")

            if not token:
                print(f"{Colors.YELLOW}Trying get token again...{Colors.RESET}")
                return solve_captcha()
            else:
                print(
                    f"{Colors.GREEN}{Icons.SUCCESS} Captcha token obtained successfully{Colors.RESET}"
                )
                return token

        except Exception as e:
            print(
                f"{Colors.RED}{Icons.ERROR} Error getting token: {str(e)}{Colors.RESET}"
            )
            return None

        finally:
            try:
                driver.quit()
            except:
                pass

    except Exception as e:
        print(
            f"{Colors.RED}{Icons.ERROR} Error initializing driver: {str(e)}{Colors.RESET}"
        )
        return None


def start_session(address, captcha_token):
    url = "https://faucet-testnet.singularityfinance.ai/api/startSession"
    payload = {
        "addr": address,
        "captchaToken": captcha_token,
    }

    try:
        response = requests.post(url, headers=HEADERS, json=payload)

        if response.status_code == 200:
            data = response.json()
            print(
                f"{Colors.GREEN}{Icons.SUCCESS} Session status: {data['status']}{Colors.RESET}"
            )

            if "session" in data:
                return data["session"]
            else:
                print(
                    f"{Colors.YELLOW}{Icons.WARNING} Response data: {data}{Colors.RESET}"
                )

                if data.get("failedCode") == "RECURRING_LIMIT":
                    print(
                        f"{Colors.RED}{Icons.ERROR} You have reached the session creation limit. Please try again later.{Colors.RESET}"
                    )
                return None
        else:
            print(
                f"{Colors.RED}{Icons.ERROR} Error starting session: {response.text}{Colors.RESET}"
            )
            return None

    except Exception as e:
        print(f"{Colors.RED}{Icons.ERROR} Request error: {str(e)}{Colors.RESET}")
        return None


def claim_reward(session, captcha_token):
    url = "https://faucet-testnet.singularityfinance.ai/api/claimReward"
    payload = {
        "session": session,
        "captchaToken": captcha_token,
    }

    try:
        response = requests.post(url, headers=HEADERS, json=payload)

        if response.status_code == 200:
            data = response.json()
            print(
                f"{Colors.GREEN}{Icons.SUCCESS} Claim status: {data['status']}{Colors.RESET}"
            )
        else:
            print(
                f"{Colors.RED}{Icons.ERROR} Error claiming reward: {response.text}{Colors.RESET}"
            )

    except Exception as e:
        print(f"{Colors.RED}{Icons.ERROR} Request error: {str(e)}{Colors.RESET}")


if __name__ == "__main__":
    address = input(f"{Colors.BLUE}Enter Address: {Colors.RESET}")

    print(f'{Colors.BOLD}{"="*50}{Colors.RESET}')
    print(f"{Colors.BLUE}{Icons.PROCESS} Starting faucet claim process{Colors.RESET}")

    captcha_token = solve_captcha()
    if not captcha_token:
        print(f"{Colors.RED}{Icons.ERROR} Failed to obtain captcha token{Colors.RESET}")
        exit()

    session = start_session(address, captcha_token)
    if not session:
        print(f"{Colors.RED}{Icons.ERROR} Failed to start session{Colors.RESET}")
        exit()

    print(f"{Colors.YELLOW}{Icons.INFO} Waiting before claim...{Colors.RESET}")
    time.sleep(3)

    captcha_token = solve_captcha()
    if not captcha_token:
        print(
            f"{Colors.RED}{Icons.ERROR} Failed to obtain captcha token for claim{Colors.RESET}"
        )
        exit()

    claim_reward(session, captcha_token)
    print(f'{Colors.BOLD}{"="*50}{Colors.RESET}')
