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


def naturalKeys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def humanSort(list_of_strings_with_number):
    return sorted(list_of_strings_with_number, key=naturalKeys)


def getDataFrames():
    dataFrames = dict((samplePath, pd.read_excel(samplePath))
        for samplePath in glob.glob(os.path.join('data', '*.xlsx')))

    return dataFrames


def getDataFrameWithAllMZDataFramesTogether():
    scriptDirPath = os.path.dirname(__file__)
    dataDirPath = os.path.join(scriptDirPath, "data")

    listOfDataFrames = []
    for sampleFileName in humanSort(os.listdir(dataDirPath)):
        sampleFilePath = os.path.join(dataDirPath, sampleFileName)
        sampleFileNameWithoutSuffix = (str)(sampleFileName.split(".")[0])
        firstColName = sampleFileNameWithoutSuffix + " " + MZ_NAME
        secondColName = sampleFileNameWithoutSuffix + " " + INTENSITY_NAME
        curr_data_frame = pd.read_excel(sampleFilePath,
                                        names=[firstColName, secondColName])[firstColName]
        listOfDataFrames.append(curr_data_frame)

    return pd.concat(listOfDataFrames, axis=1)


def getDataFrameWithAllDataFramesTogether():
    scriptDirPath = os.path.dirname(__file__)
    dataDirPath = os.path.join(scriptDirPath, "data")

    listOfDataFrames = []
    for sampleFileName in humanSort(os.listdir(dataDirPath)):
        sampleFilePath = os.path.join(dataDirPath, sampleFileName)
        sampleFileNameWithoutSuffix = (str)(sampleFileName.split(".")[0])
        firstColName = sampleFileNameWithoutSuffix + " " + MZ_NAME
        secondColName = sampleFileNameWithoutSuffix + " " + INTENSITY_NAME
        listOfDataFrames.append(pd.read_excel(sampleFilePath, names=[firstColName, secondColName]))

    return pd.concat(listOfDataFrames, axis=1)


def show_plots(n=5):
    samples = getDataFrames()
    for i, (sampleName, df) in enumerate(list(samples.items())[:5]):
        print('configuring {} ({} records)...'.format(sampleName, df.shape[0]))
        # plt.figure(i)
        df['min'] = df.iloc[argrelextrema(df.Intensity.values, np.less_equal, order=n)[0]]['Intensity']
        df['max'] = df.iloc[argrelextrema(df.Intensity.values, np.greater_equal, order=n)[0]]['Intensity']
        print('found {} max points: {}'.format(len(df[df['max'].notnull()]['max']), df[df['max'].notnull()]))
        plt.scatter(df.MZ, df['min'], c='r')
        plt.scatter(df.MZ, df['max'], c='g')
        plt.plot(df.MZ, df.Intensity)
        # plt.scatter(df.MZ, df.Intensity)
        plt.title(sampleName)

    plt.show()


def getCurrColumnFromColumnNameInAllMzData(currColumnNameInAllMzData):
    sampleName = currColumnNameInAllMzData.split(" ")[0]
    return int(sampleName.split("sample")[1]) - 1


def fillMatchedMZDataFrame(allMzData, matchedMZDataFrame, row, column, currNumber):
    matchedMZDataFrame.iloc[row, column] = currNumber
    currValue = allMzData.iloc[row, column]
    lowerThreshold = currValue * (100 - PPM / 1000000) / 100
    upperThreshold = currValue * (100 + PPM / 1000000) / 100

    for currColumnNameInAllMzData in allMzData.iloc[:, column + 1:]:

        matchedRowsInCurrColumnIndex = allMzData.loc[(allMzData[currColumnNameInAllMzData] >= lowerThreshold) &
                                                    (allMzData[currColumnNameInAllMzData] <= upperThreshold)].index
        if(not matchedRowsInCurrColumnIndex.empty):
            matchColumn = getCurrColumnFromColumnNameInAllMzData(currColumnNameInAllMzData)
            matchRow = matchedRowsInCurrColumnIndex.item()
            matchedMZDataFrame.iloc[matchRow, matchColumn] = currNumber


def getDataFrameFilledWithMatchedMZ(allMzData):

    # initialize the matchedMZDataFrame
    shape = allMzData.shape
    numberOfRows = shape[0]
    numberOfColumns = shape[1]
    matchedMZDataFrame = pd.DataFrame(index=range(numberOfRows), columns=range(numberOfColumns))
    # matchedMZDataFrame[0] = np.arange(number_of_rows)

    # initialize the number need for iterating
    currNumber = 0

    # iteration over the df
    for column in matchedMZDataFrame:
        currMatchedMZDataFrameColumn = matchedMZDataFrame[column]
        for items in currMatchedMZDataFrameColumn.iteritems():
            row = items[0]
            value = items[1]
            if(pd.isna(value)):
                fillMatchedMZDataFrame(allMzData, matchedMZDataFrame, row, column, currNumber)
                currNumber += 1


    print("done")


def main():
    # allData = getDataFrameWithAllDataFramesTogether()
    allMZData = getDataFrameWithAllMZDataFramesTogether()
    matchedMz = getDataFrameFilledWithMatchedMZ(allMZData)


    # samples = getDataFrames()
    # joined = pd.concat(df.MZ for df in samples.values())
    # columns = ['MZ_{}'.format(os.path.basename(sampleName)) for sampleName in samples.keys()]
    # table = pd.DataFrame({'Samples': joined}, columns=['Samples', ] + columns)
    # for sampleName, df in samples.items():
    #     table['MZ_{}'.format(os.path.basename(sampleName))] = [i if i in df.values else np.NaN for i in table.Samples]
    #
    # table.save


    print("done")

if __name__ == '__main__':
    main()

