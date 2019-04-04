import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import re
# import numpy as np

MZ_NAME = "MZ"
INTENSITY_NAME = "Intensity"


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def humanSort(list_of_strings_with_number):
    return sorted(list_of_strings_with_number, key=natural_keys)


def getDataFrameWithAllDataFramesTogether():
    script_dir_path = os.path.dirname(__file__)
    data_dir_path = os.path.join(script_dir_path, "data")

    list_of_data_frames = []
    for sample_file_name in humanSort(os.listdir(data_dir_path)):
        sample_file_path = os.path.join(data_dir_path, sample_file_name)
        sample_file_name_without_suffix = (str)(sample_file_name.split(".")[0])
        first_col_name = sample_file_name_without_suffix + " " + MZ_NAME
        second_col_name = sample_file_name_without_suffix + " " + INTENSITY_NAME
        list_of_data_frames.append(
            pd.read_excel(sample_file_path, names=[first_col_name, second_col_name]))

    return pd.concat(list_of_data_frames, axis=1)


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


def getPanelContainingAllDataFrames():
    script_dir_path = os.path.dirname(__file__)
    data_dir_path = os.path.join(script_dir_path, "data")

    dict_of_sample_name_and_data = {}

    for sample_file_name in os.listdir(data_dir_path):
        sample_file_name_without_suffix = sample_file_name.split(".")[0]
        sample_file_path = os.path.join(data_dir_path, sample_file_name)
        dict_of_sample_name_and_data[sample_file_name_without_suffix] = \
            pd.read_excel(sample_file_path, names=[MZ_NAME, INTENSITY_NAME])

    return pd.Panel(dict_of_sample_name_and_data)


def main():
    # all_data = getDataFrameWithAllDataFramesTogether()
    all_MZ_data = getDataFrameWithAllMZDataFramesTogether()
    print("done")



if __name__ == '__main__':
    main()
