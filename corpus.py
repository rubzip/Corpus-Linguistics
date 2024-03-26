from lxml import etree
import pandas as pd
import os
import re

# Initization of aprser:
parser = etree.XMLParser(remove_blank_text=True)

# First of all we are going to check the category of every article
fname1 = "./data/ground-truth-validation-bypublisher-20181122.xml"
tree = etree.parse(fname1, parser)

# is_hyperpartasian is going to store if a particular id is or not hyperpartasian
is_hyperpartasian = dict()
data = []
for article in tree.xpath("/articles/article"):
    id = article.get('id')
    hyperpartasian = article.get('hyperpartisan')
    bias = article.get('bias')
    url = article.get('url')
    
    data.append((id, hyperpartasian, bias, url))
    is_hyperpartasian[id] = (hyperpartasian=='true')
df1 = pd.DataFrame(data, columns=['id', 'hyperpartasian', 'bias', 'url'])

# Now we are going to store an article in a different file depending if it is hyperpartasian
fname2 = "./data/articles-validation-bypublisher-20181122.xml"
tree = etree.parse(fname2, parser)

if not os.path.exists("articles"):
    os.mkdir("articles")

open("articles/hyperpartasian.txt", 'w', encoding="utf8").close()
open("articles/non-hyperpartasian.txt", 'w', encoding="utf8").close()

data = []
for article in tree.xpath("/articles/article"):
    id, title, date = article.get('id'), article.get('title'), article.get('published-at')
    data.append((id, title, date))
    
    if is_hyperpartasian[id]:
        path = f"articles/hyperpartasian.txt"
    else:
        path = f"articles/non-hyperpartasian.txt"
    
    content = ""
    for p in article.xpath(".//p"):
        content += str(p.xpath("string()")) + '\n'

    with open(path, 'a', encoding="utf8") as file:
        file.write(content)
                
df2 = pd.DataFrame(data, columns=['id', 'title', 'publication'])
pd.merge(df1, df2, on='id').to_csv("content.csv")