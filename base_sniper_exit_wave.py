import requests, time
from collections import defaultdict

def sniper_exit_wave():
    print("Base — Sniper Exit Wave (10+ big sells in <3 min)")
    seen_pairs = set()
    sells = defaultdict(int)

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/transactions/base?limit=500")
            for tx in r.json().get("transactions", []):
                pair = tx["pairAddress"]
                age = time.time() - tx.get("timestamp", 0)

                if age > 180: continue  # старше 3 мин

                if tx.get("side") != "sell" or tx.get("valueUSD", 0) < 15000:
                    continue

                if pair not in seen_pairs:
                    sells[pair] = 0
                    seen_pairs.add(pair)

                sells[pair] += 1

                if sells[pair] >= 10:
                    token = tx["token0"]["symbol"] if "WETH" in tx["token1"]["symbol"] else tx["token1"]["symbol"]
                    print(f"SNIPER EXIT WAVE\n"
                          f"{token} — {sells[pair]} big sells in {age:.0f}s\n"
                          f"https://dexscreener.com/base/{pair}\n"
                          f"→ Snipers cashing out — dump incoming\n"
                          f"{'EXIT'*30}")
                    del sells[pair]

        except:
            pass
        time.sleep(1.5)

if __name__ == "__main__":
    sniper_exit_wave()
