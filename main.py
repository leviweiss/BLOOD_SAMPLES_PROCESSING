import pandas as pd
import os

MZ_NAME = "MZ"
INTENSITY_NAME = "Intensity"

def getDataFrameWithAllDataFramesTogether():
    script_dir_path = os.path.dirname(__file__)
    data_dir_path = os.path.join(script_dir_path, "data")

    list_of_data_frames = []
    for sample_file_name in os.listdir(data_dir_path):
        sample_file_path = os.path.join(data_dir_path, sample_file_name)
        list_of_data_frames.append(pd.read_excel(sample_file_path, names=[MZ_NAME, INTENSITY_NAME]))

    return pd.concat(list_of_data_frames, axis=1)


def getPanelContainingAllDataFrames():
    script_dir_path = os.path.dirname(__file__)
    data_dir_path = os.path.join(script_dir_path, "data")

    dict_of_sample_name_and_data = {}

    for sample_file_name in os.listdir(data_dir_path):
        sample_file_name_without_suffix = sample_file_name.split(".")[0]
        sample_file_path = os.path.join(data_dir_path, sample_file_name)
        dict_of_sample_name_and_data[sample_file_name_without_suffix] = pd.read_excel(sample_file_path, names=[MZ_NAME, INTENSITY_NAME])

    return pd.Panel(dict_of_sample_name_and_data)


def main():
    panel = getPanelContainingAllDataFrames()




if __name__ == '__main__':
    main()
