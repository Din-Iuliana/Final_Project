import requests
import json
import re

URL_RE = re.compile(r"https?://\S+")

def clean_body(text: str) -> str:
    if not text or text in ("[deleted]", "[removed]"):
        return ""

    text = URL_RE.sub("", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

url = "https://www.reddit.com/r/Romania/comments/1pknq3z/%C3%AEn_seara_asta_se_anun%C8%9B%C4%83_cel_mai_de_amploare.json"

headers = {
    "User-Agent": "conversation-sentiment-script/0.1 (by u/your_username)"
}

response = requests.get(url, headers=headers)
response.raise_for_status()

resp = response.json()

# sanity check (this would have caught your KeyError case)
if not (isinstance(resp, list) and len(resp) >= 2):
    raise TypeError(f"Unexpected Reddit JSON shape: {type(resp)}")

with open("./resp.json", "w", encoding="utf-8") as f:
    json.dump(resp, f, ensure_ascii=False, indent=2)

def prune_listing(listing):
    keep = {"id", "parent_id", "author", "created_utc", "body"}

    def recurse(children):
        pruned = []
        for item in children:
            if item.get("kind") != "t1":
                continue

            d = item["data"]

            raw_body = d.get("body", "")
            clean_text = clean_body(raw_body)

            clean_data = {k: d.get(k) for k in keep}
            clean_data["body"] = clean_text
            clean_data["is_deleted"] = raw_body == "[deleted]"
            clean_data["is_removed"] = raw_body == "[removed]"

            replies = d.get("replies")
            clean_replies = recurse(replies["data"]["children"]) if isinstance(replies, dict) else []

            pruned.append({"kind": "t1", "data": clean_data, "replies": clean_replies})
        return pruned

    return recurse(listing["data"]["children"])

with open("./resp_clean.json", "w", encoding="utf-8") as f:
    json.dump(prune_listing(resp[1]), f, ensure_ascii=False, indent=2)








def comments(listing):
    def recurse(children):
        pruned = []
        for item in children:
            if item.get("kind") != "t1":
                continue

            d = item["data"]
            raw_body = d.get("body", "")
            clean_text = clean_body(raw_body)


            replies = d.get("replies")
            clean_replies = recurse(replies["data"]["children"]) if isinstance(replies, dict) else []

            pruned.append({"data": clean_text, "replies": clean_replies})
        return pruned

    return recurse(listing["data"]["children"])

with open("./comments.json", "w", encoding="utf-8") as f:
    json.dump(comments(resp[1]), f, ensure_ascii=False, indent=2)




