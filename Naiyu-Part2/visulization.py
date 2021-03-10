import scattertext as st
from scattertext import SampleCorpora, whitespace_nlp_with_sentences
from data_center import *
from scattertext import produce_scattertext_explorer
from scattertext.CorpusFromPandas import CorpusFromPandas
from scattertext.termscoring.ScaledFScore import ScaledFScorePresets
import pandas as pd
import matplotlib.pyplot as plt
import jieba

data_center = DataCenter()

dates = data_center.read_json(type="date")
titles = data_center.read_json(type="title")
texts = data_center.read_json(type="text")

new_titles = [jieba.lcut(title) for title in titles]
stop_words = [word.strip('\n') for word in open("data/stopwords.txt", "r").readlines()]
filterd_titles = []
for title in new_titles:
    filterd_title = []
    for word in title:
        if word.lower() not in stop_words and word not in stop_words:
            filterd_title.append(word)
    filterd_titles.append("".join(filterd_title))
print(filterd_titles)

raw_df = pd.DataFrame()
raw_df['text'] = filterd_titles
raw_df['party'] = ['bill' for i in range(len(filterd_titles))]
raw_df['speaker'] = ['None' for i in range(len(filterd_titles))]
df = raw_df.assign(
    parse=lambda raw_df: raw_df.text.apply(st.whitespace_nlp_with_sentences))
corpus = st.CorpusWithoutCategoriesFromParsedDocuments(
    df, parsed_col='parse'
).build().get_unigram_corpus().remove_infrequent_words(minimum_term_count=6)

dispersion = st.Dispersion(corpus)

dispersion_df = dispersion.get_df()
print(dispersion_df.head(3))
dispersion_df = dispersion_df.assign(
    X=lambda df: df.Frequency,
    Xpos=lambda df: st.Scalers.log_scale(df.X),
    Y=lambda df: df["Rosengren's S"],
    Ypos=lambda df: st.Scalers.scale(df.Y)
)
html = st.dataframe_scattertext(
    corpus,
    plot_df=dispersion_df,
    metadata=corpus.get_df()['speaker'] + ' (' + corpus.get_df()['party'].str.upper() + ')',
    ignore_categories=True,
    x_label='Log Frequency',
    y_label="Rosengren's S",
    y_axis_labels=['More Dispersion', 'Medium', 'Less Dispersion']
)
fn = 'output/visualization.html'
open(fn, 'wb').write(html.encode('utf-8'))
print('open ' + fn)