import spacy
from collections import defaultdict
import pandas as pd

def clean_line(nlp, line):
    return ' '.join([token.text for token in nlp(line.lower()) if not token.is_stop])

def count_words(nlp, fname):
    counter = defaultdict(int)
    with open(fname, 'r', encoding="utf8") as f:
        for line in f:
            for token in clean_line(nlp, line):
                counter[token] += 1
    return counter

def count_bigrams(nlp, fname):
    counter = defaultdict(int)
    with open(fname, 'r', encoding="utf8") as f:
        for line in f:
            cleaned_line = clean_line(nlp, line)
            for t1, t2 in zip(cleaned_line[:-1], cleaned_line[1:]):
                counter[t1, t2] += 1
    return counter

import spacy
from collections import defaultdict
import pandas as pd

def clean_line(nlp, line):
    return ' '.join([token.text for token in nlp(line.lower()) if not token.is_stop])

def clean_file(fname, fname_out):
    with open(fname, 'r', encoding="utf-8") as f:
        content = f.read()
        
    nlp = spacy.load("en_core_web_sm")
    text = clean_line(nlp, content)
    
    with open(fname_out, 'w', encoding="utf-8") as f:
        f.write(text)
    
    print(f"File {fname} cleaned into {fname_out}")

clean_file("articles/hyperpartasian.txt", "articles/hyperpartasian-clean.txt")
clean_file("articles/non-hyperpartasian.txt", "articles/non-hyperpartasian-clean.txt")





nlp = spacy.load("en_core_web_sm")

hyperpartisan = count_words(nlp, "./articles/hyperpartisan")
df_hyperpartisan = pd.DataFrame.from_dict(hyperpartisan, columns=["hyperpartisan_freq"])

non_hyperpartisan = count_words(nlp, "./articles/non-hyperpartisan")
df_non_hyperpartisan = pd.DataFrame.from_dict(non_hyperpartisan, columns=["non_hyperpartisan_freq"])

freqs = pd.merge(df_hyperpartisan, df_non_hyperpartisan)
freqs.to_csv("frequencies.csv")