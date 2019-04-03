import pandas as pd
import os

def main():
    MZ_NAME = "MZ"
    INTENSITY_NAME = "Intensity"

    script_dir_path = os.path.dirname(__file__)
    data_dir_path = os.path.join(script_dir_path, "data")

    abs_file_path = os.path.join(script_dir_path, "data/sample1.xlsx")
    data1 = pd.read_excel(abs_file_path, names=[MZ_NAME, INTENSITY_NAME])

    abs_file_path = os.path.join(script_dir_path, "data/sample2.xlsx")
    data2 = pd.read_excel(abs_file_path, names=[MZ_NAME, INTENSITY_NAME])

    df_col = pd.concat([data1, data2], axis=1)

    data = pd.DataFrame()
    for sample_file_name in os.listdir(data_dir_path):
        sample_file_path = os.path.join(data_dir_path, sample_file_name)
        data = data + pd.read_excel(sample_file_path, names=[MZ_NAME, INTENSITY_NAME])




if __name__ == '__main__':
    main()
