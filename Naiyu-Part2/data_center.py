import pandas as pd
import json
import jieba
from tqdm import tqdm
from collections import Counter
from nltk.corpus import words

class DataCenter():
    def __init__(self):
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
                    and word.lower() not in stop_words:
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

