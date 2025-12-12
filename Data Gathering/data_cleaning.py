from helpers import clean_body

def clean_1(json):
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

    return recurse(json["data"]["children"])
