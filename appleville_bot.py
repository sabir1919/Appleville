import requests
import time
import sys
import random
from colorama import Fore, init

init(autoreset=True)

CYCLE_DELAY = 30  # seconds between each cycle (adjust if needed)
ITEM_KEY = "golden-apple"  # item to buy & plant

# =========================
# Progress Bar with Live Points
# =========================
def progress_bar(seconds, account_name, cookie, message="⏳ Next cycle in"):
    total = seconds
    for elapsed in range(total):
        remaining = total - elapsed
        percent = int((elapsed / total) * 100)
        bar_length = 30
        filled = int(bar_length * elapsed // total)
        bar = "█" * filled + "░" * (bar_length - filled)

        # Color changes
        if remaining > total * 0.6:
            color = Fore.GREEN
        elif remaining > total * 0.3:
            color = Fore.YELLOW
        else:
            color = Fore.RED

        # 🔄 Fetch live points
        points_text = ""
        if cookie:
            try:
                url = "https://app.appleville.xyz/api/trpc/core.getPoints?batch=1"
                headers = {"Cookie": cookie, "Content-Type": "application/json"}
                r = requests.post(url, headers=headers, json={})
                if r.status_code == 200:
                    data = r.json()
                    points = data[0]["result"]["data"]["json"]["points"]
                    points_text = f"💰 {points} pts"
                else:
                    points_text = "💰 --"
            except:
                points_text = "💰 --"

        sys.stdout.write(
            f"\r{Fore.CYAN}👤 {account_name} | {color}{message}: [{bar}] {percent}% ({remaining}s left) | {points_text}"
        )
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r" + " " * 120 + "\r")  # clear line


# =========================
# Bot Actions
# =========================
def harvest(cookie, proxy=None):
    url = "https://app.appleville.xyz/api/trpc/core.harvest?batch=1"
    headers = {"Cookie": cookie, "Content-Type": "application/json"}
    data = {"0": {"json": {"slotIndexes": [4]}}}
    try:
        r = requests.post(url, headers=headers, json=data, proxies=proxy, timeout=15)
        if r.status_code == 200:
            print(Fore.GREEN + "✅ Harvested successfully!")
        else:
            print(Fore.RED + f"❌ Harvest failed: {r.text}")
    except Exception as e:
        print(Fore.RED + f"⚠️ Harvest error: {e}")


def buy_item(cookie, proxy=None):
    url = "https://app.appleville.xyz/api/trpc/core.buyItem?batch=1"
    headers = {"Cookie": cookie, "Content-Type": "application/json"}
    data = {"0": {"json": {"purchases": [{"key": ITEM_KEY, "quantity": 1}]}}}
    try:
        r = requests.post(url, headers=headers, json=data, proxies=proxy, timeout=15)
        if r.status_code == 200:
            print(Fore.GREEN + f"✅ Bought item: {ITEM_KEY}")
        else:
            print(Fore.RED + f"❌ Buy failed: {r.text}")
    except Exception as e:
        print(Fore.RED + f"⚠️ Buy error: {e}")


def plant_seed(cookie, proxy=None):
    url = "https://app.appleville.xyz/api/trpc/core.plantSeed?batch=1"
    headers = {"Cookie": cookie, "Content-Type": "application/json"}
    data = {"0": {"json": {"plantings": [{"slotIndex": 4, "seedKey": ITEM_KEY}]}}}
    try:
        r = requests.post(url, headers=headers, json=data, proxies=proxy, timeout=15)
        if r.status_code == 200:
            print(Fore.GREEN + f"✅ Planted seed: {ITEM_KEY}")
        else:
            print(Fore.RED + f"❌ Plant failed: {r.text}")
    except Exception as e:
        print(Fore.RED + f"⚠️ Plant error: {e}")


# =========================
# Proxy Loader
# =========================
def load_proxies():
    try:
        with open("proxy.txt", "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        return proxies
    except FileNotFoundError:
        return []


def get_proxy(proxy_line):
    if not proxy_line:
        return None
    return {"http": f"http://{proxy_line}", "https": f"http://{proxy_line}"}


# =========================
# Main Bot Loop
# =========================
def main():
    # Load cookies
    try:
        with open("cookies.txt", "r") as f:
            cookies = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + "❌ cookies.txt not found!")
        return

    proxies = load_proxies()

    while True:
        for i, cookie in enumerate(cookies):
            proxy_line = random.choice(proxies) if proxies else None
            proxy = get_proxy(proxy_line)

            account_name = f"Account {i+1}"
            print(Fore.MAGENTA + f"\n=== 🚀 Running {account_name} with proxy: {proxy_line or 'None'} ===")

            harvest(cookie, proxy)
            buy_item(cookie, proxy)
            plant_seed(cookie, proxy)

            # ⏳ Wait cycle with live points
            progress_bar(CYCLE_DELAY, account_name, cookie, message="⏳ Next cycle in")


if __name__ == "__main__":
    main()
