from collections import defaultdict
import pandas as pd
import re

def tokenize(line):
    # This function takes a line, converts it to lowercase, filters any non letter char and splits it 
    return re.sub(r"([^a-z])+", ' ', line.lower()).split()

def count_words(fname):
    counter = defaultdict(int)
    with open(fname, 'r', encoding="utf8", errors="ignore") as f:
        for line in f:
            for token in tokenize(line):
                counter[token] += 1
    return counter

def count_bigrams(fname):
    counter = defaultdict(int)
    with open(fname, 'r', encoding="utf8", errors="ignore") as f:
        for line in f:
            clean_line = tokenize(line)
            for t1, t2 in zip(clean_line[:-1], clean_line[1:]):
                counter[t1, t2] += 1
    return counter

hyperpartisan = count_words("./articles/hyperpartasian.txt")
print("hyperpartisan done")
df_hyperpartisan = pd.DataFrame.from_dict(
    hyperpartisan, 
    columns=["hyperpartisan_freq"], 
    orient="index"
)

non_hyperpartisan = count_words("./articles/non-hyperpartasian.txt")
print("non hyperpartisan done")
df_non_hyperpartisan = pd.DataFrame.from_dict(
    non_hyperpartisan, 
    columns=["non_hyperpartisan_freq"], 
    orient="index"
)

freqs = pd.merge(df_hyperpartisan, df_non_hyperpartisan)
freqs.to_csv("frequencies.csv")