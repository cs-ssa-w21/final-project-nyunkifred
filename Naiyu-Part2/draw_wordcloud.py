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
        font_path="./msyh.ttc",
        colormap=colormaps[i],
        min_font_size=10,
        max_font_size=49,
        collocations=False,
        width=600
    )
    wc.generate(",".join(word_list))
    wc.to_file("output/"+str(i)+"_wordCloud.png")