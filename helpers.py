import re
from constants import URL_RE 

# This fucntion cleans the url specific code from a comment body
def clean_body(text: str) -> str:
    if not text or text in ("[deleted]", "[removed]"):
        return ""

    text = URL_RE.sub("", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

