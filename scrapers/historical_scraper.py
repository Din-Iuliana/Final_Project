import requests
import time
from utils.csv_writer import append_to_csv
from utils.rate_limit import rate_limit

PUSHIFT_URL = "https://api.pullpush.io/reddit/search/submission"

def fetch_historical(subreddit, total=5000, batch_size=500):
    saved_rows = 0
    last_timestamp = None
    output_file = f"./data/raw/historical_{subreddit}.csv"

    print(f"\n[Historical] Starting for r/{subreddit}...")

    while saved_rows < total:
        params = {
            "subreddit" : subreddit,
            "size" : batch_size,
            "sort" : "desc",
            "sort_type" : "created_utc"
        }

        if last_timestamp:
            params["before"] = last_timestamp


        # retry logic 
        for attempt in range(5):
            try:
                resp = requests.get(PUSHIFT_URL,params=params,timeout=10)
                resp.raise_for_status()
                break
            except:
                time.time_sleep(2** attempt)       
        else:
            print("[Historical] Max retries reached. Stopping.")       


        data = resp.json().get("data",[])
        if not data:
            print("[Historical] No more data available.")
            break

        append_to_csv(output_file,data)

        saved_rows += len(data)
        last_timestamp = data[-1]["created_utc"]

        print(f"[Historical] Saved {saved_rows}/{total}")

        rate_limit()

    print(f"[Historical] DONE. Saved: {output_file}")              


    