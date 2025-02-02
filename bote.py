import requests
import random
import time
import string
from fake_useragent import UserAgent
from colorama import Fore, Style, init


init(autoreset=True)


banner = f"""{Fore.RED}==============================
{Fore.GREEN}=    {Fore.YELLOW}Auto Reff Ecosapiens    {Fore.GREEN}=
{Fore.BLUE}=    {Fore.MAGENTA}From ADFMIDN TEAM     {Fore.BLUE}=
{Fore.RED}==============================
"""
print(banner)

def generate_email():
    prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{prefix}@gmail.com"

def generate_evm():
    return "0x" + ''.join(random.choices("abcdef" + string.digits, k=40))


def submit_referral(ref_code, jumlah):
    for i in range(1, jumlah + 1):
        email = generate_email()
        evm_address = generate_evm()
        user_agent = UserAgent().random  
        delay = random.randint(5, 35)  

        headers = {
            "User-Agent": user_agent,
            "Content-Type": "application/json",
            "Origin": "https://ecosapiens.xyz",
            "Referer": "https://ecosapiens.xyz/",
        }

        heartbeat_payload = {
            "location": f"https://ecosapiens.xyz/pages/airdrop?ref_id={ref_code}",
            "waitlist_id": "24495",
            "referrer": "",
            "widget_type": "WIDGET_1"
        }
        hb_response = requests.post("https://api.getwaitlist.com/api/v1/widget_heartbeats", json=heartbeat_payload, headers=headers)
        if hb_response.status_code == 200:
            heartbeat_uuid = hb_response.json().get("uuid")
            print(f"{Fore.GREEN}[✓] Heartbeat sukses: {heartbeat_uuid}")
        else:
            print(f"{Fore.RED}[✗] Gagal Heartbeat: {hb_response.text}")
            continue

        referral_payload = {
            "waitlist_id": 24495,
            "referral_link": f"https://ecosapiens.xyz/pages/airdrop?ref_id={ref_code}",
            "heartbeat_uuid": heartbeat_uuid,
            "widget_type": "WIDGET_1",
            "email": email,
            "answers": [
                {
                    "question_value": "What is your EVM wallet address?",
                    "answer_value": evm_address
                }
            ]
        }
        ref_response = requests.post("https://api.getwaitlist.com/api/v1/waiter", json=referral_payload, headers=headers)

        if ref_response.status_code == 200:
            print(f"{Fore.GREEN}[✓] Referral {i} sukses: {email} -> {evm_address}")
        else:
            print(f"{Fore.RED}[✗] Referral {i} gagal: {ref_response.text}")

        print(f"{Fore.YELLOW}[!] Menunggu {delay} detik sebelum referral berikutnya...\n")
        time.sleep(delay)


        if i % 5 == 0:
            print(f"{Fore.CYAN}[⏳] Sudah {i} referral, jeda 5 jam sebelum lanjut...")
            time.sleep(18000)  


ref_code = input(f"{Fore.CYAN}Masukkan kode referral: {Style.RESET_ALL}")
jumlah = int(input(f"{Fore.CYAN}Masukkan jumlah referral: {Style.RESET_ALL}"))

print(f"{Fore.YELLOW}[!] Memulai proses dengan kode referral {ref_code} untuk {jumlah} referral...\n")
submit_referral(ref_code, jumlah)

print(f"{Fore.GREEN}[✓] Proses selesai! Semua referral telah dikirim.")
