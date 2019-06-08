import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import seaborn as sns
import re
from scipy.signal import argrelextrema


sys.path.insert(0, os.path.dirname(__file__))

MZ_NAME = "MZ"
INTENSITY_NAME = "Intensity"
PPM = 5


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def humanSort(list_of_strings_with_number):
    return sorted(list_of_strings_with_number, key=natural_keys)


def get_data_frames():
    data_frames = dict((sample_path, pd.read_excel(sample_path))
        for sample_path in glob.glob(os.path.join('data', '*.xlsx')))
    
    return data_frames


def getDataFrameWithAllMZDataFramesTogether():
    script_dir_path = os.path.dirname(__file__)
    data_dir_path = os.path.join(script_dir_path, "data")

    list_of_data_frames = []
    for sample_file_name in humanSort(os.listdir(data_dir_path)):
        sample_file_path = os.path.join(data_dir_path, sample_file_name)
        sample_file_name_without_suffix = (str)(sample_file_name.split(".")[0])
        first_col_name = sample_file_name_without_suffix + " " + MZ_NAME
        second_col_name = sample_file_name_without_suffix + " " + INTENSITY_NAME
        curr_data_frame = pd.read_excel(sample_file_path,
                                        names=[first_col_name, second_col_name])[first_col_name]
        list_of_data_frames.append(curr_data_frame)

    return pd.concat(list_of_data_frames, axis=1)


def getDataFrameWithAllDataFramesTogether():
    script_dir_path = os.path.dirname(__file__)
    data_dir_path = os.path.join(script_dir_path, "data")

    list_of_data_frames = []
    for sample_file_name in humanSort(os.listdir(data_dir_path)):
        sample_file_path = os.path.join(data_dir_path, sample_file_name)
        sample_file_name_without_suffix = (str)(sample_file_name.split(".")[0])
        first_col_name = sample_file_name_without_suffix + " " + MZ_NAME
        second_col_name = sample_file_name_without_suffix + " " + INTENSITY_NAME
        list_of_data_frames.append(pd.read_excel(sample_file_path, names=[first_col_name, second_col_name]))
        
    return pd.concat(list_of_data_frames, axis=1)


def show_plots(n=5):
    samples = get_data_frames()
    for i, (sample_name, df) in enumerate(list(samples.items())[:5]):
        print('configuring {} ({} records)...'.format(sample_name, df.shape[0]))
        # plt.figure(i)
        df['min'] = df.iloc[argrelextrema(df.Intensity.values, np.less_equal, order=n)[0]]['Intensity']
        df['max'] = df.iloc[argrelextrema(df.Intensity.values, np.greater_equal, order=n)[0]]['Intensity']
        print('found {} max points: {}'.format(len(df[df['max'].notnull()]['max']), df[df['max'].notnull()]))
        plt.scatter(df.MZ, df['min'], c='r')
        plt.scatter(df.MZ, df['max'], c='g')
        plt.plot(df.MZ, df.Intensity)
        # plt.scatter(df.MZ, df.Intensity)
        plt.title(sample_name)

    plt.show()


def fillMatchedMZDataFrame(matchedMZDataFrame, row, column, curr_number):
    pass


def getDataFrameFilledWithMatchedMZ(all_MZ_data):

    # initialize the matchedMZDataFrame
    shape = all_MZ_data.shape
    number_of_rows = shape[0]
    number_of_columns = shape[1]
    matchedMZDataFrame = pd.DataFrame(index=range(number_of_rows), columns=range(number_of_columns))
    # matchedMZDataFrame[0] = np.arange(number_of_rows)

    # initialize the number need for iterating
    curr_number = number_of_columns

    # iteration over the df
    for column in matchedMZDataFrame:
        currMatchedMZDataFrameColumn = matchedMZDataFrame[column]
        for items in currMatchedMZDataFrameColumn.iteritems():
            row = items[0]
            value = items[1]
            if(pd.isna(value)):
                fillMatchedMZDataFrame(matchedMZDataFrame, row, column, curr_number)


    print("done")


def main():
    # all_data = getDataFrameWithAllDataFramesTogether()
    all_MZ_data = getDataFrameWithAllMZDataFramesTogether()
    matched_mz = getDataFrameFilledWithMatchedMZ(all_MZ_data)


    # samples = get_data_frames()
    # joined = pd.concat(df.MZ for df in samples.values())
    # columns = ['MZ_{}'.format(os.path.basename(sample_name)) for sample_name in samples.keys()]
    # table = pd.DataFrame({'Samples': joined}, columns=['Samples', ] + columns)
    # for sample_name, df in samples.items():
    #     table['MZ_{}'.format(os.path.basename(sample_name))] = [i if i in df.values else np.NaN for i in table.Samples]
    #
    # table.save


    print("done")

if __name__ == '__main__':
    main()
    
