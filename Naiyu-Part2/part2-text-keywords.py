# PART 2: TEXT PROCESSING AND KEYWORDS

# STEP 1: CONSTRUCT A DATA CENTER
import pandas as pd
import json
import jieba
from tqdm import tqdm
from collections import Counter
from nltk.corpus import words

class DataCenter():
    def __init__(self):
        """
        Construct a class that processes raw data
        """
        self.ori_type = ['date', 'no', 'title', 'text']

    def read_json(self, filename='data/bills.json', type="title"):
        """
        Selectively read data according to type
        :param filename:
        :param type:
        :return:
        """
        assert type in self.ori_type
        id = self.ori_type.index(type)
        print(f"read the {type} data in {filename} ing......")
        df = pd.read_json(filename, orient='columns')
        data = df.values[id]  # 1590
        print(data[:5])
        return data

    def preprocess_data(self, datas):
        """
        Perform data preprocessing on the data obtained
        from the original json file: split words; stopwords;
        lowercase conversion.
        :param datas:
        :return:
        """
        stop_words = [word.strip('\n') for word in \
            open("data/stopwords.txt", "r").readlines()]
        new_datas = []
        for data in tqdm(datas):
            new_data = []
            splited_data = jieba.lcut(data)
            for word in splited_data:
                if word.lower() in words.words() \
                    and word.lower() not in stop_words: # use words and stopaords to filter
                    new_data.append(word.lower())
            new_datas.append(new_data)
        print(new_datas[:5])
        return new_datas

    @staticmethod
    def counter_frequency(datas, save_filename=None):
        """
        Count the word frequency of the data after data preprocessing.
        If save path is specified, the word frequency is saved.
        :param datas:
        :param save_filename:
        :return:
        """
        word_list = []
        for data in datas:
            for word in data:
                word_list.append(word)
        # counter
        counter = Counter(word_list)
        dictionary = dict(counter)
        if save_filename:
            print(f"write frequency into {save_filename}")
            with open(save_filename, "w") as f:
                for key in dictionary.keys():
                    f.write(str(key) + "\t" + str(dictionary[key]) + "\n")
        return dictionary

    @staticmethod
    def topk_frequency(dictionary, k=20, save_filename=None):
        """
        This is used to sort words according to frequency.
        """
        sorted_word = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)[:20]
        if save_filename:
            print(f"top_{k}write into{save_filename}")
            with open(save_filename, "w") as f:
                for turple_ in sorted_word:
                    f.write(turple_[0] + "\t" + str(turple_[1]) + "\n")
        return sorted_word

    @staticmethod
    def date_transform(dates):
        """
        This is used to pre-process the date.
        """
        date2month = {}
        for date in dates:
            month, day, year = date.split("/")
            new_rep = year + month
            date2month[date] = new_rep
        return date2month

    @staticmethod
    def collect_databy_date(datas, ori_dates, datedict):
        """
        This is used to identify the date from the dictionary.
        """
        data_by_date_dict = {}
        for data, date in zip(datas, ori_dates):
            data_by_date_dict.setdefault(datedict[date], []).append(data)
        return data_by_date_dict

    @staticmethod
    def date_transform_for_plot(date):
        """
        This is for the transformation of date.
        """
        assert len(date)==6
        date2id_year = ['2019', '2020' , '2021']
        date2id_month = ['01', '02', '03', '04', '05', '06', \
            '07', '08', '09', '10', '11', '12']
        new_date = date2id_year.index(date[:4]) * 12 + \
            date2id_month.index(date[4:]) + 1
        return new_date

    @staticmethod
    def date_re_transform_for_plot(number):
        """
        This is for the transformation of date - 2.
        """
        date2id_year = ['2019', '2020', '2021']
        date2id_month = ['01', '02', '03', '04', '05', '06', \
            '07', '08', '09', '10', '11', '12']
        year = date2id_year[number // 12]
        month = date2id_month[number % 12]
        date = str(year) + "/" + str(month)
        print(date)
        return date


# STEP 2: THE NUMBER OF BILLS OVER TIME
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.pyplot import MultipleLocator
plt.rcParams['font.sans-serif'] = ['SimHei']

def main():
    """
    A function used to generate the trend of the number of bills
    """
    # utilize data center
    data_center = DataCenter()
    dates = data_center.read_json(type="date")
    titles = data_center.read_json(type="title")
    texts = data_center.read_json(type="text")
    date2month = data_center.date_transform(dates)
    # save the global information once
    if not os.path.exists("output/top_20_all_frequency.txt"):
        data = data_center.preprocess_data(titles)
        word_frequency_dict = data_center.counter_frequency(data, \
            save_filename="output/word_all_frequency.txt")
        sorted_topk = data_center.topk_frequency(word_frequency_dict, \
            save_filename="output/top_20_all_frequency.txt")
    # store all data in new order
    data_by_date_dict = data_center.collect_databy_date(texts, dates, date2month)
    # plot the number of bills
    sns.set()
    plot_data = []
    for key in data_by_date_dict.keys():
        for i in range(len(data_by_date_dict[key])):
            result = data_center.date_transform_for_plot(key)
            plot_data.append(result)
    xlabel = []
    for i in range(28):
        print(i)
        xlabel.append(data_center.date_re_transform_for_plot(i))
    sns.distplot(plot_data,
                 color='darkblue')
    x_major_locator = MultipleLocator(1)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    plt.xlim(0, 28)
    plt.xticks(np.arange(28), xlabel, rotation=270)
    # plt.show()

if __name__ == '__main__':
    main()


# STEP 3: EXTRACT KEYWORDS AND DRAW WORD FREQUENCY
def merge_date(year, merge_number=3):
    """
    This is to find all covid bills in a given year.
    """
    assert isinstance(year, str)
    date2id_month = ['01', '02', '03', '04', '05', '06', \
        '07', '08', '09', '10', '11', '12']
    merge_dict = {}
    for index, month in enumerate(date2id_month):
        cur_filename = "output/" + year + month + "_word_all_frequency.txt"
        merge_dict.setdefault(index//merge_number, []).append(cur_filename)
    return merge_dict

merge_dict = merge_date('2020')

stop_words = [word.strip('\n') for word in open("data/stopwords.txt", "r").readlines()]
color_list = ['Set2', 'Accent', 'BrBG', 'ocean']
color_list = ['Set2', 'Blues_r', 'BrBG', 'spring_r']
id2month_label = {0: 'Jan-Mar', 1: 'Apr-Jun', 2: "Jul-Sep", 3: 'Oct-Dec'}

for i in merge_dict.keys():
    common_words = []
    for filename in merge_dict[i]:
        with open(filename, "r") as f:
            lines = f.readlines()
            for line in lines:
                data = line.strip("\n")
                word, count = data.split("\t")[0], data.split("\t")[1]
                if word not in stop_words:
                    common_words.append((word, int(count)))
    merged_common_words = {}
    for word, count in common_words:
        merged_common_words.setdefault(word, []).append(int(count))
    for key in merged_common_words.keys():
        merged_common_words[key] = np.sum(merged_common_words[key])
    merged_common_words = sorted(merged_common_words.items(),\
         key=lambda x: x[1], reverse=True)
    print(merged_common_words)
    # write into output
    with open("output/"+str(i)+"_word_frequency.txt", "w") as f:
        for word, count in merged_common_words:
            f.write(word+"\t"+str(count)+"\n")
    df1 = pd.DataFrame(merged_common_words, columns=[id2month_label[i], 'count'])[:20]
    df1.groupby(id2month_label[i]).sum()['count'].sort_values(ascending=False).plot(
        kind='bar', colormap=color_list[i], rot=270, \
            title='Top 20 words in review after removing stop words')
    plt.savefig('output/'+str(i)+'_top20_word.png', bbox_inches='tight')
    # plt.show()


# STEP 4: DRAW WORDCLOUD
from wordcloud import WordCloud
import matplotlib.colors as colors

id2month_label = {0: 'Q1: Jan-Mar', 1: 'Q2: Apr-Jun', \
    2: "Q3: Jul-Sep", 3: 'Q4: Oct-Dec'}
stop_words = [word.strip('\n') for word \
    in open("data/stopwords.txt", "r").readlines()]

for i in range(4):
    filename = "output/" + str(i) + "_word_frequency.txt"
    word_list = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            data = line.strip("\n")
            word, count = data.split("\t")[0], data.split("\t")[1]
            if word not in stop_words:
                for j in range(int(count)):
                    word_list.append(word)
    colormaps = [colors.ListedColormap(['#B0E0E6', '#9ACD32', '#40E0D0', '#FFF68F']),
                 colors.ListedColormap(['#CD5C5C', '#8B4513', '#8B658B', '#FFC1C1']),
                 colors.ListedColormap(['#8B8B00', '#FFD700', '#CDAD00', '#EEEE00']),
                 colors.ListedColormap(['#FF7F50', '#FF8C00', '#FFA07A', '#E9967A'])]

    # plot wordclouds
    wc = WordCloud(
        background_color="white",
        max_words=300,
        # font_path="./msyh.ttc",
        colormap=colormaps[i],
        min_font_size=10,
        max_font_size=49,
        collocations=False,
        width=600
    )
    print(word_list)
    wc.generate(",".join(word_list))
    wc.to_file("output/"+str(i)+"_wordCloud.png")


# STEP 5: DRAW SCATTERPLOT
import scattertext as st
from scattertext import SampleCorpora, whitespace_nlp_with_sentences
from scattertext import produce_scattertext_explorer
from scattertext.CorpusFromPandas import CorpusFromPandas
from scattertext.termscoring.ScaledFScore import ScaledFScorePresets
# Construct data center
data_center = DataCenter()
dates = data_center.read_json(type="date")
titles = data_center.read_json(type="title")
texts = data_center.read_json(type="text")
# Draw plot
new_titles = [jieba.lcut(title) for title in titles]
stop_words = [word.strip('\n') for word \
    in open("data/stopwords.txt", "r").readlines()]
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
    metadata=corpus.get_df()['speaker'] \
        + ' (' + corpus.get_df()['party'].str.upper() + ')',
    ignore_categories=True,
    x_label='Log Frequency',
    y_label="Rosengren's S",
    y_axis_labels=['More Dispersion', 'Medium', 'Less Dispersion']
)
fn = 'output/visualization.html'
open(fn, 'wb').write(html.encode('utf-8'))
print('open ' + fn)
