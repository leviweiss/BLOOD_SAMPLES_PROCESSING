import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import sklearn
import seaborn as sns
import re

from scipy.signal import argrelextrema

sys.path.insert(0, os.path.dirname(__file__))


MZ_NAME = "MZ"
INTENSITY_NAME = "Intensity"


def get_data_frames():
    data_frames = dict((sample_path, pd.read_excel(sample_path))
        for sample_path in glob.glob(os.path.join('data', '*.xlsx')))
    
    return data_frames


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


// shai's code
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


def main():

    all_data = getDataFrameWithAllDataFramesTogether()
    all_MZ_data = getDataFrameWithAllMZDataFramesTogether()
    
    // shai's code
    samples = get_data_frames()
    joined = pd.concat(df.MZ for df in samples.values())
    columns = ['MZ_{}'.format(os.path.basename(sample_name)) for sample_name in samples.keys()]
    table = pd.DataFrame({'Samples': joined}, columns=['Samples', ] + columns)
    for sample_name, df in samples.items():
        table['MZ_{}'.format(os.path.basename(sample_name))] = [i if i in df.values else np.NaN for i in table.Samples]

    table.save  
    return table

    print("done")

if __name__ == '__main__':
    main()
    
