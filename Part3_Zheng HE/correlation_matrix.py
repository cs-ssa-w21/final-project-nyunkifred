'''
MACS 30122 W'21: Final Project

Zheng HE

This file contains all the code for the third and last part of the Final Project.
In this file, I sorted out all of the six keywords which appear in all of the
four quarterly top-20 lists provided by Naiyu Jiang's part and mapped six possible
indicators onto the patterns of these keywords via a correlation matrix and a
heatmap based upon that matrix.
'''

import csv
import pandas as pd
import dataframe_image as dfi
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def convert_txt():
    '''
    Convert Naiyu's word frequency lists into readable csv file for merging.
    
    return:
        quarter_1_df (dataframe): raw dataframe with the keywords and their
        frequency values in the 1st quarter of 2020 together in a single solumn
        separated by "\t"
        quarter_2_df (dataframe): raw dataframe with the keywords and their
        frequency values in the 2nd quarter of 2020 together in a single solumn
        separated by "\t"
        quarter_3_df (dataframe): raw dataframe with the keywords and their
        frequency values in the 3rd quarter of 2020 together in a single solumn
        separated by "\t"
        quarter_4_df (dataframe): raw dataframe with the keywords and their
        frequency values in the 4th quarter of 2020 together in a single solumn
        separated by "\t"
    '''
    first_quarter = pd.read_csv("data/0_word_frequency.txt")
    first_quarter.to_csv("data/0_word_frequency.csv", index = None)
    second_quarter = pd.read_csv("data/1_word_frequency.txt")
    second_quarter.to_csv("data/1_word_frequency.csv", index = None)
    third_quarter = pd.read_csv("data/2_word_frequency.txt")
    third_quarter.to_csv("data/2_word_frequency.csv", index = None)
    fourth_quarter = pd.read_csv("data/3_word_frequency.txt")
    fourth_quarter.to_csv("data/3_word_frequency.csv", index = None)
    
    quarter_1_df = pd.read_csv("data/0_word_frequency.csv", header = None)
    quarter_2_df = pd.read_csv("data/1_word_frequency.csv", header = None)
    quarter_3_df = pd.read_csv("data/2_word_frequency.csv", header = None)
    quarter_4_df = pd.read_csv("data/3_word_frequency.csv", header = None)
    
    return (quarter_1_df, quarter_2_df, quarter_3_df, quarter_4_df)


def separate_columns(df):
    '''
    Separate the frequency values from the keywords column and put the former
    into a new column called "frequency"; then get the four dataframes, each
    containing the keywords whose frequencies are within the top-20 each quarter.
    These dataframes are in accordance with Naiyu's outputs of quarterly top-20
    words graphs.
    
    Input:
        df (dataframe): the four dataframe outputs of the "convert_txt()" function.
    Return:
        top_20_lst: a dataframe containing the keywords whose frequencies are 
        within the top-20 in that quarter.
    '''
    df.columns = ['contents']
    quarter_df = df["contents"].str.split("\t", n = 1, expand = True)
    quarter_df.columns = ['keyword', 'frequency']
    top_20_lst = quarter_df.head(20)
    
    return top_20_lst


def merge_top_20_lists():
    '''
    Merge the four top-20 keyword dataframes into a big one dataframe. In this
    new dataframe, only the keywords that appear in all the four top-20 keyword
    dataframes as well as their quarterly frequencies are kept.
    
    Return:
        top_20_q14 (dataframe): a dataframe that contains five columns: keyword,
        keyword's frequency in the 1st quarter of 2020, keyword's frequency in 
        the 2nd quarter of 2020, keyword's frequency in the 3rd quarter of 2020, 
        and keyword's frequency in the 4th quarter of 2020.
    '''
    top_20_q1 = separate_columns(convert_txt()[0])
    top_20_q2 = separate_columns(convert_txt()[1])
    top_20_q3 = separate_columns(convert_txt()[2])
    top_20_q4 = separate_columns(convert_txt()[3])
    
    top_20_q12 = top_20_q1.merge(top_20_q2, how='inner', on='keyword')
    top_20_q13 = top_20_q12.merge(top_20_q3, how='inner', on='keyword')
    top_20_q14 = top_20_q13.merge(top_20_q4, how='inner', on='keyword')
    top_20_q14.columns = ['keyword', '2020_qt1', '2020_qt2',\
                          '2020_qt3', '2020_qt4']
    
    return top_20_q14


def append_us_covid_growth_data():
    '''
    Append the US covid-19 data to the dataframe. The US covid-19 data is from
    the New York Times' "covid-19-data" on Github (Yeah, NY Times has an offi-
    cial Github account!!! Link: https://github.com/nytimes/covid-19-data ). 
    At the bottom of the database there is a file called "us.csv" which records
    the cumulative covid-19 positive cases and deaths inside the U.S. by day. 
    
    We figured out the numbers of quarterly covid-19 positive cases and deaths
    by subtracting the last-day figure of a quarter by the last-day figure of
    the immediately previous quarter. For example, in order to get the number
    of deaths in the 2nd quarter of 2020, we subtract the deaths number on June
    30, 2020 by the deaths number on March 31, 2020.
    
    As the numbers of quarterly covid-19 positive cases kept increasing in 2020,
    which does not fit the general trends of the frequency of top-20 keywords,
    we thought it might be wiser to calculate the growth rates of quarterly 
    covid-19 positive cases and deaths since there were ups and downs in their
    growth rates and thus it is more easy for us to see the interactions between
    the covid-19 pandemic and the frequency of top-20 keywords.

    Return:
        df_ten_factors (dataframe): a dataframe containing ten rows: 6 keywords
        and their frequencies; us_covid_positive -- total number of positive
        covid-19 cases in each quarter of 2020; us_covid_positive_case_growth 
        rate % -- quarterly growth rate of positive covid-19 cases; us_covid_death
        -- total number of covid-19 deaths in each quarter of 2020; us_covid_death
        _growth rate % -- quarterly growth rate of covid-19 deaths.
    '''
    df_six_keywords = merge_top_20_lists()
    us_covid_df = pd.read_csv("data/us.csv", header=None)
    us_covid_df.columns = ['date', 'cases', 'deaths']
    
    for i in range(len(us_covid_df)):
        if us_covid_df['date'][i] == '2020-03-31':
            qt_1_positive = us_covid_df['cases'][i]
            qt_1_death = us_covid_df['deaths'][i]
            
    for j in range(len(us_covid_df)):
        if us_covid_df['date'][j] == '2020-06-30':
            qt_1_to_2_positive = us_covid_df['cases'][j]
            qt_1_to_2_death = us_covid_df['deaths'][j]
            
    for k in range(len(us_covid_df)):
        if us_covid_df['date'][k] == '2020-09-30':
            qt_1_to_3_positive = us_covid_df['cases'][k]
            qt_1_to_3_death = us_covid_df['deaths'][k]
            
    for m in range(len(us_covid_df)):
        if us_covid_df['date'][m] == '2020-12-31':
            qt_1_to_4_positive = us_covid_df['cases'][m]
            qt_1_to_4_death = us_covid_df['deaths'][m]
    
    qt_2_positive = int(qt_1_to_2_positive) - int(qt_1_positive)
    qt_3_positive = int(qt_1_to_3_positive) - int(qt_1_to_2_positive)
    qt_4_positive = int(qt_1_to_4_positive) - int(qt_1_to_3_positive)
    
    qt_2_death = int(qt_1_to_2_death) - int(qt_1_death)
    qt_3_death = int(qt_1_to_3_death) - int(qt_1_to_2_death)
    qt_4_death = int(qt_1_to_4_death) - int(qt_1_to_3_death)
    
    qt_1_positive_growth_rate = 1 * 100
    qt_2_positive_growth_rate = ((qt_2_positive - int(qt_1_positive)) /\
                                 int(qt_1_positive)) * 100
    qt_3_positive_growth_rate = ((qt_3_positive - qt_2_positive) /\
                                 qt_2_positive) * 100
    qt_4_positive_growth_rate = ((qt_4_positive - qt_3_positive) /\
                                 qt_3_positive) * 100
    
    qt_1_death_growth_rate = 1 * 100
    qt_2_death_growth_rate = ((qt_2_death - int(qt_1_death)) /\
                              int(qt_1_death)) * 100
    qt_3_death_growth_rate = ((qt_3_death - qt_2_death) / qt_2_death) * 100
    qt_4_death_growth_rate = ((qt_4_death - qt_3_death) / qt_3_death) * 100
    
    us_covid_positive_row = pd.DataFrame([["us_covid_positive", qt_1_positive,\
                                            qt_2_positive, qt_3_positive,\
                                            qt_4_positive]])
    us_covid_positive_row.columns = ['keyword', '2020_qt1', '2020_qt2',\
                                      '2020_qt3', '2020_qt4']
    
    us_covid_death_row = pd.DataFrame([["us_covid_death", qt_1_death,\
                                            qt_2_death, qt_3_death,\
                                            qt_4_death]])
    us_covid_death_row.columns = ['keyword', '2020_qt1', '2020_qt2',\
                                      '2020_qt3', '2020_qt4']
    
    us_covid_positive_growth_row = pd.DataFrame([["us_covid_positive_case_growth rate %",\
                                            qt_1_positive_growth_rate,\
                                            qt_2_positive_growth_rate,\
                                            qt_3_positive_growth_rate,\
                                            qt_4_positive_growth_rate]])
    us_covid_positive_growth_row.columns = ['keyword', '2020_qt1', '2020_qt2',\
                                      '2020_qt3', '2020_qt4']
    
    us_covid_death_growth_row = pd.DataFrame([["us_covid_death_growth rate %",\
                                            qt_1_death_growth_rate,\
                                            qt_2_death_growth_rate,\
                                            qt_3_death_growth_rate,\
                                            qt_4_death_growth_rate]])
    us_covid_death_growth_row.columns = ['keyword', '2020_qt1', '2020_qt2',\
                                      '2020_qt3', '2020_qt4']
    
    df_seven_factors = df_six_keywords.append(us_covid_positive_row,\
                                              ignore_index = True)
    df_eight_factors = df_seven_factors.append(us_covid_positive_growth_row,\
                                              ignore_index = True)
    df_nine_factors = df_eight_factors.append(us_covid_death_row,\
                                              ignore_index = True)
    df_ten_factors = df_nine_factors.append(us_covid_death_growth_row,\
                                              ignore_index = True)
    
    return df_ten_factors


def append_us_unemployment_rate():
    '''
    Append the US unemployment rate to the dataframe. Here we used the OECD data
    (Link: https://data.oecd.org/unemp/unemployment-rate.htm ) where the quarterly
    unemployment rates of the U.S. are provided in a downloadable csv file. 
    
    Return:
        df_eleven_factors (dataframe): a dataframe containing eleven rows inclu-
        ding the newly appended US unemployment rate row.
    '''
    OECD_csv = pd.read_csv("data/OECD_USunemploymentrate.csv", header = None)
    
    us_unemployent_row = pd.DataFrame([["us_unemployment_rate %", OECD_csv[6][1],\
                                        OECD_csv[6][2], OECD_csv[6][3],\
                                        OECD_csv[6][4]]])
    us_unemployent_row.columns = ['keyword', '2020_qt1', '2020_qt2',\
                                '2020_qt3', '2020_qt4']
    df_ten_factors = append_us_covid_growth_data()
    df_eleven_factors = df_ten_factors.append(us_unemployent_row,\
                                        ignore_index = True)
   
    return df_eleven_factors


def append_us_productivity():
    '''
    Append the last group of data -- US labor productivity -- to the dataframe.
    The data is from the U.S. Bureau of Labor Statistics (Link: https://data.bl
    s.gov/timeseries/PRS85006092?amp%253bdata_tool=XGtable&output_view=data&inc
    lude_graphs=true ). Labor productivity here means "percent change from pre-
    vious quarter at annual rate" according to the U.S. Bureau of Labor Statis-
    tics.
    
    Return:
        df_final (dataframe): the finalized dataframe containing the original 
        data of 12 factors: 6 keywords and their quarterly fequencies, 6 para-
        meters and their quarterly values.
    '''
    us_prod_xlsx = pd.read_excel("data/US_BLS_productivity.xlsx", header = None)
    
    us_prod_temp1 = us_prod_xlsx.drop([5], axis = 1)
    us_prod_temp2 = us_prod_temp1.drop(index = range(0, 11), axis = 0)
    us_prod_temp2.columns = ['year', 'qt1', 'qt2', 'qt3', 'qt4']
    
    prod_qt_1 = us_prod_temp2["qt1"][21]
    prod_qt_2 = us_prod_temp2["qt2"][21]
    prod_qt_3 = us_prod_temp2["qt3"][21]
    prod_qt_4 = us_prod_temp2["qt4"][21]
    
    us_prod_row = pd.DataFrame([["us_productivity %", prod_qt_1, prod_qt_2,\
                                 prod_qt_3, prod_qt_4]])
    us_prod_row.columns = ['keyword', '2020_qt1', '2020_qt2',\
                           '2020_qt3', '2020_qt4']
    
    df_eleven_factors = append_us_unemployment_rate()
    df_final = df_eleven_factors.append(us_prod_row,\
                                        ignore_index = True)
    
    return df_final


def generate_correlation_matrix():
    '''
    Generate the correlation matrix based upon the "df_final" dataframe. Since
    the final heatmap does not leave much space for the names of these factors,
    we need to shorten them by giving them abbreviations, but the order of these
    abbreviations are the same with their original counterparts in the "df_final"
    dataframe.
    
    Return:
        corr_matr (dataframe): A 12 * 12 correlation matrix consisting of all
        12 factors (6 keywords and 6 parameters) and the correlation coefficients
        between each other.
    '''
    df = append_us_productivity()
    
    df["keyword"][0] = "eme"
    df["keyword"][1] = "rel"
    df["keyword"][2] = "res"
    df["keyword"][3] = "car"
    df["keyword"][4] = "bus"
    df["keyword"][5] = "acc"
    df["keyword"][6] = "pos"
    df["keyword"][7] = "pos_gr"
    df["keyword"][8] = "dea"
    df["keyword"][9] = "dea_gr"
    df["keyword"][10] = "unem"
    df["keyword"][11] = "prod"
    
    df_1 = df.transpose()
    df_2 = df_1.rename(columns=df_1.iloc[0])
    df_3 = df_2.drop(["keyword"])
    corr_matr = df_3.astype('float64').corr()
   
    return corr_matr


def generate_heatmap():
    '''
    Generate the heatmap of the correlation matrix.
    
    Return:
        heatmap_no_figure (picture): The heatmap of the correlation matrix.
    '''    
    corr_matrix = generate_correlation_matrix()
    heatmap_no_figure = sns.heatmap(corr_matrix)
    
    return heatmap_no_figure


def output_files():
    '''
    Generate the png files of three significant outputs: 1) finalized dataframe
    containing the original data of 12 factors; 2) correlation matrix based upon
    the finalized dataframe; 3) the heatmap showing the correlation matrix.
    '''
    df_final = append_us_productivity()
    dfi.export(df_final, "output/df_final.png")
    
    corr_matr = generate_correlation_matrix()
    dfi.export(corr_matr, "output/correlation_matrix.png")
    
    heatmap_no_figure = generate_heatmap()
    heatmap = heatmap_no_figure.get_figure()    
    heatmap.savefig('output/heatmap_no_figure.png', dpi = 400)
    
    return None