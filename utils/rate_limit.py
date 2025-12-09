import time
import random

def rate_limit(max_wait=0.5, min_wait=1.5):
    time.sleep(random.uniform(max_wait,min_wait))
