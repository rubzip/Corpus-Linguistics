from fun import count_words
import pandas as pd

hyperpartisan = count_words("../articles/hyperpartasian.txt")
print("hyperpartisan done")
df_hyperpartisan = pd.DataFrame.from_dict(
    hyperpartisan,
    columns=["hyperpartisan_freq"],
    orient="index"
)

non_hyperpartisan = count_words("../articles/non-hyperpartasian.txt")
print("non hyperpartisan done")
df_non_hyperpartisan = pd.DataFrame.from_dict(
    non_hyperpartisan, 
    columns=["non_hyperpartisan_freq"],
    orient="index"
)

freqs = pd.merge(df_hyperpartisan, df_non_hyperpartisan, left_index=True, right_index=True)
freqs.to_csv("/word_frequencies.csv")