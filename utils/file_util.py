import os 

def ensure_directories():
    if not os.path.exists("./data/raw"):
        os.makedirs("./data/raw")
       
