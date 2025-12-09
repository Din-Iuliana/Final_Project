import pandas as pd
import os

def append_to_csv(path, rows):
    df = pd.DataFrame(rows)
    header = not os.path.exists(path)
    df.to_csv(path, mode="a", header=header, index=False)
