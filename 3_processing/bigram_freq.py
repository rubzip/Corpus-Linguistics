import pandas as pd
import numpy as np
import re

# Loading data
df = pd.read_csv("./bigram_frequencies.csv", index_col=0)
df.index = df.index.set_names(['bigram_text'])
df = df.reset_index()

# bigram to tuple
def str2tuple(x):
    match = re.match(r"\(\'(.+)\'.+\'(.+)\'", x)
    if match:
        return (match.group(1), match.group(2))
df['bigram'] = df['bigram_text'].map(str2tuple)

# Number of articles:
articles = pd.read_csv("./content.csv")
N_hyperpartasian = articles["hyperpartasian"].sum()
N_non_hyperpartasian = len(articles) - N_hyperpartasian

# Filtering Stopwords:
with open("stopwords.txt", 'r') as f:
    stopwords = set(f.read().split())
contains_stopword = df["bigram"].map(lambda x: (x[0] in stopwords) or (x[1] in stopwords))
df = df[~contains_stopword]

# Filtering bt frequencies
df["freq"] = df["non_hyperpartisan_freq"] + df["hyperpartisan_freq"]
frequent = (df[["hyperpartisan_freq", "non_hyperpartisan_freq"]] >= 20).all(axis=1)
df = df[frequent]

# Results:
df["p_hyperpartisan"] = df["hyperpartisan_freq"] / N_hyperpartasian
df["p_non_hyperpartisan"] = df["non_hyperpartisan_freq"] / N_non_hyperpartasian

df["o_hyperpartisan"] = df["p_hyperpartisan"] / (1 - df["p_hyperpartisan"])
df["o_non_hyperpartisan"] = df["p_non_hyperpartisan"] / (1 - df["p_non_hyperpartisan"])

df["r"] = np.log(df["o_hyperpartisan"] / df["o_non_hyperpartisan"])

# Taking the top 50 words
non_hyper = df.sort_values("r").head(50).reset_index(drop=True)
hyper = df.sort_values("r", ascending=False).head(50).reset_index(drop=True)
pd.concat([hyper, non_hyper]).to_csv("word_highest.csv", index=False)