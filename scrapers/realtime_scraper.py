import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import random

from utils.csv_writer import append_to_csv
from utils.rate_limit import rate_limit

def scrape_realtime(subreddit, limit=500, keyword=None):
    url = f"https://old.reddit.com/r/{subreddit}/new/"
    output_file = f"data/raw/realtime_{subreddit}.csv"

    headers = {
        "User-Agent": f"Mozilla/5.0 (Random UA {random.randint(1,99999)})"
    }

    posts_collected = 0
    last_titles_seen = set()

    print(f"\n[Realtime] Starting LIVE scraping for r/{subreddit}...")

    while posts_collected < limit:
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
        except:
            print("[Realtime] Request failed. Retrying...")
            time.sleep(3)
            continue

        entries = soup.find_all("div", class_="thing")

        current_titles = set()
        rows_to_save = []

        for item in entries:
            title_tag = item.find("a", class_="title")
            if not title_tag:
                continue

            title = title_tag.text.strip()
            current_titles.add(title)

            if keyword and keyword.lower() not in title.lower():
                continue

            rows_to_save.append({
                "timestamp": datetime.utcnow().isoformat(),
                "subreddit": subreddit,
                "title": title,
                "score": item.get("data-score"),
                "url": item.get("data-url"),
                "id": item.get("data-fullname"),
                "keyword_matched": keyword or "",
            })

        # detectare de pagini identice (evită infinite loops)
        if current_titles == last_titles_seen:
            print("[Realtime] Same page detected. Slowing down...")
            time.sleep(5)
            continue

        last_titles_seen = current_titles

        if rows_to_save:
            append_to_csv(output_file, rows_to_save)
            posts_collected += len(rows_to_save)

            print(f"[Realtime] Saved {posts_collected}/{limit}")

        # mergi la pagina următoare
        next_button = soup.find("span", class_="next-button")
        if not next_button:
            print("[Realtime] No more pages.")
            break

        url = next_button.find("a")["href"]

        rate_limit()

    print(f"[Realtime] DONE. Saved: {output_file}")
