Part 3: Creating the keywords-parameters dataframe, generating the correlation matrix and the heatmap

The PART3-Correlation_Matrix_Heatmap-Zheng_He folder contains several files:

correlation_matrix.py: The code of Part 3 that generates the three output files.

data (folder): A folder containing the data introduced and used in "correlation_matrix.py".

    0_word_frequency.txt: a text file containing all the keywords and their frequencies from the bills during the 1st quarter of 2020;

    1_word_frequency.txt: a text file containing all the keywords and their frequencies from the bills during the 2nd quarter of 2020;

    2_word_frequency.txt: a text file containing all the keywords and their frequencies from the bills during the 3rd quarter of 2020;

    3_word_frequency.txt: a text file containing all the keywords and their frequencies from the bills during the 4th quarter of 2020.

    The above files are the output files of Naiyu Jiang's part.
    
    OECD_USunemploymentrate.csv: an XLS file containing the quarterly unemployment rate of the US in 2020. The source of this file is:
            https://data.oecd.org/unemp/unemployment-rate.htm 

    us.csv: an XLS file containing daily numbers of accumutive COVID-19 positive cases and deaths in the US since January 2020. The source
            of this file is: https://github.com/nytimes/covid-19-data

    US_BLS_productivity.xlsx: an XLS file containing the quarterly labor productivity change rates of the US in 2020. The source of this
            file is: https://data.bls.gov/timeseries/PRS85006092?amp%253bdata_tool=XGtable&output_view=data&include_graphs=true				

output (folder): A folder containing three output files of this final group project.

    df_final.png: the final dataframe containing twelve factors (six keywords and six independent variables (parameters)), on which the
            correlation matrix (correlation_matrix.png) is based;

    correlation_matrix.png: the correlation matrix showing the coefficients between two factors;

    heatmap_no_figure.png: the heatmap reflecting the correlation matrix with colors and shades.