import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# draw word frequency chart every 3 months

def merge_date(year, merge_number=3):
    assert isinstance(year, str)
    date2id_month = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    merge_dict = {}
    for index, month in enumerate(date2id_month):
        cur_filename = "output/" + year + month + "_word_all_frequency.txt"
        merge_dict.setdefault(index//merge_number, []).append(cur_filename)
    return merge_dict

merge_dict = merge_date('2020')

# stopwords
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
    merged_common_words = sorted(merged_common_words.items(), key=lambda x: x[1], reverse=True)
    print(merged_common_words)
    exit()
    with open("output/"+str(i)+"_word_frequency.txt", "w") as f:
        for word, count in merged_common_words:
            f.write(word+"\t"+str(count)+"\n")
    df1 = pd.DataFrame(merged_common_words, columns=[id2month_label[i], 'count'])[:20]

    df1.groupby(id2month_label[i]).sum()['count'].sort_values(ascending=False).plot(
        kind='bar', colormap=color_list[i], rot=270, title='Top 20 words in review after removing stop words')
    plt.savefig('output/'+str(i)+'_top20_word.png', bbox_inches='tight')
    plt.show()