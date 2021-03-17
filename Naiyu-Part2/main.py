from data_center import *
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.pyplot import MultipleLocator
plt.rcParams['font.sans-serif'] = ['SimHei']

def main():
    # construct data center
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
    # store all data under the new order
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
    plt.show()

if __name__ == '__main__':
    main()