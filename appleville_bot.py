import requests, time, uuid, re, os

COOKIES_FILE = "cookies.txt"

def load_cookies():
    if not os.path.exists(COOKIES_FILE):
        print(f"❌ Missing {COOKIES_FILE}, please create it with your cookie string")
        exit()
    return open(COOKIES_FILE).read().strip()

def get_meta_hash():
    url = "https://app.appleville.xyz/"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, cookies=parse_cookie_dict(load_cookies()))
    match = re.search(r'"x-meta-hash"\s*:\s*"([a-f0-9]{64})"', r.text)
    if match:
        meta = match.group(1)
        print(f"🔑 Latest x-meta-hash: {meta}")
        return meta
    print("⚠️ Could not find x-meta-hash, using fallback")
    return "432793e091906336415ec70862ce8b00cb2eb23620208080363a838be032ad09"

def parse_cookie_dict(cookie_string):
    cookies = {}
    for part in cookie_string.split(";"):
        if "=" in part:
            k, v = part.strip().split("=", 1)
            cookies[k] = v
    return cookies

def get_headers(meta_hash):
    return {
        "Referer": "https://app.appleville.xyz/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
        "content-type": "application/json",
        "sec-ch-ua": '"Chromium";v="130", "Mises";v="130", "Not?A_Brand";v="99", "Google Chrome";v="130"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "trpc-accept": "application/jsonl",
        "x-client-time": str(int(time.time() * 1000)),
        "x-meta-hash": meta_hash,
        "x-trace-id": uuid.uuid4().hex,
        "x-trpc-source": "nextjs-react",
        "cookie": load_cookies()
    }

def harvest(slot_index, meta_hash):
    url = "https://app.appleville.xyz/api/trpc/core.harvest?batch=1"
    payload = {"0": {"json": {"slotIndexes": [slot_index]}}}
    r = requests.post(url, headers=get_headers(meta_hash), json=payload)
    print("🌱 Harvest:", r.status_code, r.text[:200])

def buy(item_key, quantity, meta_hash):
    url = "https://app.appleville.xyz/api/trpc/core.buyItem?batch=1"
    payload = {"0": {"json": {"purchases": [{"key": item_key, "quantity": quantity}]}}}
    r = requests.post(url, headers=get_headers(meta_hash), json=payload)
    print("🛒 Buy:", r.status_code, r.text[:200])

def plant(slot_index, seed_key, meta_hash):
    url = "https://app.appleville.xyz/api/trpc/core.plantSeed?batch=1"
    payload = {"0": {"json": {"slotIndex": slot_index, "seedKey": seed_key}}}
    r = requests.post(url, headers=get_headers(meta_hash), json=payload)
    print("🌳 Plant:", r.status_code, r.text[:200])

if __name__ == "__main__":
    print("=== 🚀 Running Appleville Bot ===")
    meta_hash = get_meta_hash()  # auto fetch latest
    
    harvest(4, meta_hash)               # Example: harvest slot 4
    buy("golden-apple", 1, meta_hash)   # Example: buy 1 golden apple
    plant(4, "golden-apple", meta_hash) # Example: plant golden apple in slot 4
