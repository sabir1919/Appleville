import requests
import time
import random
from colorama import Fore, Style, init

# Init colors
init(autoreset=True)

# Load cookies from file
with open("cookies.txt", "r") as f:
    COOKIES = f.read().strip()

# Load proxy list
try:
    with open("proxy.txt", "r") as f:
        PROXIES = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    PROXIES = []

# Create session
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Cookie": COOKIES,
})

def debug_request(method, url, **kwargs):
    """Wrapper to log headers + response for debugging"""
    print(Fore.YELLOW + f"\n=== DEBUG {method.upper()} {url} ===")
    print(Fore.CYAN + "Headers being sent:")
    for k, v in session.headers.items():
        print(f"{k}: {v}")
    if "headers" in kwargs:
        for k, v in kwargs["headers"].items():
            print(f"{k}: {v}")
    print(Fore.CYAN + "=============================")

    try:
        if method.lower() == "get":
            resp = session.get(url, **kwargs)
        else:
            resp = session.post(url, **kwargs)

        print(Fore.MAGENTA + f"Response Status: {resp.status_code}")
        print(Fore.WHITE + resp.text[:500])  # print only first 500 chars
        return resp
    except Exception as e:
        print(Fore.RED + f"❌ Request failed: {e}")
        return None

def harvest():
    url = "https://app.appleville.xyz/api/harvest"  # adjust if wrong
    resp = debug_request("post", url, json={})
    return resp

def buy():
    url = "https://app.appleville.xyz/api/buy"
    resp = debug_request("post", url, json={"item": "seed"})
    return resp

def plant():
    url = "https://app.appleville.xyz/api/plant"
    resp = debug_request("post", url, json={"seed": "basic"})
    return resp

def get_points():
    url = "https://app.appleville.xyz/api/points"
    resp = debug_request("get", url)
    if resp and resp.status_code == 200:
        try:
            return resp.json().get("points", 0)
        except:
            return 0
    return 0

def main():
    proxy = None
    if PROXIES:
        proxy = random.choice(PROXIES)
        session.proxies.update({
            "http": proxy,
            "https": proxy
        })

    print(Fore.GREEN + f"=== 🚀 Running Account 1 with proxy: {proxy} ===")

    while True:
        # Harvest
        print(Fore.YELLOW + "🌾 Trying to harvest...")
        harvest()

        # Buy
        print(Fore.CYAN + "🛒 Trying to buy...")
        buy()

        # Plant
        print(Fore.GREEN + "🌱 Trying to plant...")
        plant()

        # Show Points
        points = get_points()
        print(Fore.MAGENTA + f"⭐ Current Points: {points}")

        print(Fore.BLUE + "⏳ Waiting 30s before next cycle...\n")
        time.sleep(30)

if __name__ == "__main__":
    main()
