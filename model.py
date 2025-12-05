from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from hdbscan import HDBSCAN
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import re
import string


# --- DOWNLOAD DEPENDINTE NLTK ---
nltk.download("punkt")
nltk.download("stopwords")

# --- STOPWORDS ---
stop_words = set(stopwords.words("english"))

# --- FUNCTIE CURATARE TEXT ---
def clean_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = [w for w in text.split() if w not in stop_words]
    return " ".join(words)

# ----- TEXTUL TAU -----
text = """
I am posting this a bit out of annoyance, but also a bit out of necessity. I’m so tired of seeing “I only work 3 hours”, “Mouse jiggler saved my life”, “how do I work 2 WFH jobs”, “I do nothing” type of posts.

WE GET IT. However, I’d like to think the vast majority of us ACTUALLY take WFH as a privilege that we’re willing to work for. I purposely work long hours JUST to prove my effectiveness from home.

I could 200% get away with watching movies, playing games, etc. but I choose not to. Why? Bc I realize I need my job more than they need me (everyone is in the same boat, admit it or not) and WFH is the best thing that’s ever happened to me.

With all of the RTO stuff going on, PLEASE stop posting all over social media how you do nothing and get away with it. Those of us that actually value the perk of wfh and our jobs don’t deserve to lose the privilege just bc you can’t wait to brag on social media about having no workplace morals.

If you do nothing? Cool. Keep doing that. Idc…But you posting about it only worsens even your own case and future.

Is one Reddit post going to ruin the future of WFH? Of course not, however, 1000+ of them can change sentiment. Reddit pretty frequently results in high SEO rankings/ google ai responses. Executives can see this stuff, even without Reddit. So please for ALL of us (including yourselves) just stop and go play your games or watch your movies or whatever.

You’re the loud few rather than the state of WFH as a whole, where most of us actually work. Thank you for attending my ted talk.

EDIT bc this blew up: I’m glad to see the vast majority thinks posting “I don’t work ever” on social media is a bad look for WFH. However, the comment section is wild (and most also agree with this). I genuinely wish we could just force those people RTO so the 6.5K that upvoted and agree and all the sensible comments don’t get our privileges taken away just bc the few loud minority can’t resist talking about how they do nothing or “get their work done in an hour”. With all due respect, if you get your work done in an hour to four hours each day, your execs are going to assume they don’t need to have you on full time. Literally just stop posting about it. Why asking that offends you is beyond me and completely mind blowing.
"""

# ----- IMPARTIRE IN PROPOZITII -----
docs = sent_tokenize(text)

# ----- CURATARE PROPOZITII -----
clean_docs = [clean_text(d) for d in docs]

# ----- INCARCARE ENCODER -----
embedding_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

# ----- CREARE BERTopic fara UMAP si HDBSCAN pentru set mic -----
topic_model = BERTopic(
    embedding_model=embedding_model,
    hdbscan_model=None,          # Dezactivam HDBSCAN
    umap_model=None,             # Dezactivam UMAP
    calculate_probabilities=False,  # Probabilitati NU
    verbose=True
)

# ----- FIT -----
topics, _ = topic_model.fit_transform(clean_docs)

# ----- OUTPUT -----
print("\n=== TOPIC INFO ===")
print(topic_model.get_topic_info())

# Afisam toate topicurile
for topic_id in topic_model.get_topic_info().Topic:
    print(f"\n=== TOPIC {topic_id} ===")
    print(topic_model.get_topic(topic_id))