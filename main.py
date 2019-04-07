import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import sklearn

import sys
sys.path.insert(0, os.path.dirname(__file__))

MZ_NAME = "MZ"
INTENSITY_NAME = "Intensity"


def get_data_frames():
    data_frames = dict((sample_path, pd.read_excel(sample_path))
        for sample_path in glob.glob(os.path.join('data', '*.xlsx')))
    
    return data_frames


def getDataFrameWithAllDataFramesTogether():
    # script_dir_path = os.path.dirname(__file__)
    # data_dir_path = os.path.join(script_dir_path, "data")
    data_dir_path = 'data'

    data_frames = list(getDataFrames().values())
    
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


def main():
    samples = get_data_frames()
    joined = pd.concat(df.MZ for df in samples.values())
    columns = ['MZ_{}'.format(os.path.basename(sample_name)) for sample_name in samples.keys()]
    table = pd.DataFrame({'Samples': joined}, columns=['Samples', ] + columns)
    for sample_name, df in samples.items():
        table['MZ_{}'.format(os.path.basename(sample_name))] = [i if i in df.values else np.NaN for i in table.Samples]

    table.save  
    return table


if __name__ == '__main__':
    print(main())
    # show_plots(int(sys.argv[1]))
