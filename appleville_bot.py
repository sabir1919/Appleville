import requests
import time
import random
import json
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# === CONFIG ===
COOKIE_FILE = "cookies.txt"
CYCLE_DELAY = 30  # seconds between each farming cycle

# Load cookie from file
if os.path.exists(COOKIE_FILE):
    with open(COOKIE_FILE", "r") as f:
        COOKIE = f.read().strip()
else:
    print(Fore.RED + f"❌ No {COOKIE_FILE} found. Please create it and paste your cookie inside.")
    exit()

# Load proxies if available
proxies_list = []
if os.path.exists("proxy.txt"):
    with open("proxy.txt") as f:
        proxies_list = [line.strip() for line in f if line.strip()]

# API Endpoints
BASE_URL = "https://app.appleville.xyz/api/trpc/core"
HARVEST_URL = f"{BASE_URL}.harvest?batch=1"
BUY_URL = f"{BASE_URL}.buyItem?batch=1"
PLANT_URL = f"{BASE_URL}.plantSeed?batch=1"

# Headers
headers = {
    "Cookie": COOKIE,
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://app.appleville.xyz",
    "Referer": "https://app.appleville.xyz/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/116.0.0.0 Safari/537.36"
}


def get_proxy():
    if not proxies_list:
        return None
    proxy = random.choice(proxies_list)
    return {"http": proxy, "https": proxy}


def harvest(proxy=None):
    payload = {"0": {"json": {"slotIndexes": [4]}}}
    try:
        r = requests.post(HARVEST_URL, headers=headers, json=payload, proxies=proxy, timeout=15)
        if r.status_code == 200:
            print(Fore.GREEN + "✅ Harvest success:", r.text)
        else:
            print(Fore.RED + f"❌ Harvest failed: {r.text}")
    except Exception as e:
        print(Fore.RED + f"⚠️ Harvest error: {e}")


def buy(proxy=None):
    payload = {"0": {"json": {"purchases": [{"key": "golden-apple", "quantity": 1}]}}}
    try:
        r = requests.post(BUY_URL, headers=headers, json=payload, proxies=proxy, timeout=15)
        if r.status_code == 200:
            print(Fore.GREEN + "✅ Buy success:", r.text)
        else:
            print(Fore.RED + f"❌ Buy failed: {r.text}")
    except Exception as e:
        print(Fore.RED + f"⚠️ Buy error: {e}")


def plant(proxy=None):
    payload = {"0": {"json": {"plantings": [{"slotIndex": 4, "seedKey": "golden-apple"}]}}}
    try:
        r = requests.post(PLANT_URL, headers=headers, json=payload, proxies=proxy, timeout=15)
        if r.status_code == 200:
            print(Fore.GREEN + "✅ Plant success:", r.text)
        else:
            print(Fore.RED + f"❌ Plant failed: {r.text}")
    except Exception as e:
        print(Fore.RED + f"⚠️ Plant error: {e}")


def get_points(proxy=None):
    try:
        url = "https://app.appleville.xyz/api/trpc/core.getUser?batch=1"
        r = requests.get(url, headers=headers, proxies=proxy, timeout=15)
        if r.status_code == 200:
            data = r.json()
            points = data[0]["result"]["data"]["json"]["points"]
            print(Fore.CYAN + f"💎 Current Points: {points}")
        else:
            print(Fore.YELLOW + f"⚠️ Could not fetch points: {r.text}")
    except Exception as e:
        print(Fore.YELLOW + f"⚠️ Points error: {e}")


def main():
    cycle = 1
    while True:
        proxy = get_proxy()
        print(Style.BRIGHT + Fore.MAGENTA + f"\n=== 🚀 Cycle {cycle} | Using Proxy: {proxy} ===")

        get_points(proxy)
        harvest(proxy)
        buy(proxy)
        plant(proxy)

        print(Fore.BLUE + f"⏳ Waiting {CYCLE_DELAY} seconds before next cycle...")
        cycle += 1
        time.sleep(CYCLE_DELAY)


if __name__ == "__main__":
    main()
