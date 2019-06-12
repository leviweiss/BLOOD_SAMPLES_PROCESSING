import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.signal import argrelextrema


sys.path.insert(0, os.path.dirname(__file__))

MZ_NAME = "MZ"
INTENSITY_NAME = "Intensity"
PPM = 5
MZFileName = "MZData.xlsx"
matchedMZFileName = "matchedMZFileName.xlsx"
MAX_COLUMN = 20
MAX_ROW = 50
TO_CUT = True


def getDataFrames():
    dataFrames = dict((samplePath, pd.read_excel(samplePath))
        for samplePath in glob.glob(os.path.join('data', '*.xlsx')))

    return dataFrames


def getDataFrameWithAllMZDataFramesTogether(dataDirPath):
    listOfDataFrames = []
    for sampleFileName in os.listdir(dataDirPath):
        sampleFilePath = os.path.join(dataDirPath, sampleFileName)
        sampleFileNameWithoutSuffix = os.path.splitext(sampleFileName)[0]
        firstColName = sampleFileNameWithoutSuffix + " " + MZ_NAME
        secondColName = sampleFileNameWithoutSuffix + " " + INTENSITY_NAME
        curr_data_frame = pd.read_excel(sampleFilePath,
                                        names=[firstColName, secondColName])[firstColName]
        listOfDataFrames.append(curr_data_frame)

    return pd.concat(listOfDataFrames, axis=1)


def getDataFrameWithAllDataFramesTogether(dataDirPath):
    listOfDataFrames = []
    for sampleFileName in os.listdir(dataDirPath):
        sampleFilePath = os.path.join(dataDirPath, sampleFileName)
        sampleFileNameWithoutSuffix = os.path.splitext(sampleFileName)[0]
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


def fillMatchedMZDataFrame(allMZData, matchedMZDataFrame, row, column, currNumber):
    matchedMZDataFrame.iloc[row, column] = currNumber
    currValue = allMZData.iloc[row, column]
    lowerThreshold = currValue - currValue * PPM / 10 ** 6
    upperThreshold = currValue + currValue * PPM / 10 ** 6

    dataframeWithTrueInPlacesWhereTheValueNeedToBe = ((allMZData.iloc[:, column + 1:] >= lowerThreshold) &
                                                      (allMZData.iloc[:, column + 1:] <= upperThreshold))

    seriesOfRowsWithTrueInPlacesWhereTheValueNeedToBe = dataframeWithTrueInPlacesWhereTheValueNeedToBe.any(axis=1)
    cuttedDataframeWithTrueInPlacesWhereTheValueNeedToBe = dataframeWithTrueInPlacesWhereTheValueNeedToBe.loc[seriesOfRowsWithTrueInPlacesWhereTheValueNeedToBe, :]
    seriesOfColumnsWithTrueIfAny = cuttedDataframeWithTrueInPlacesWhereTheValueNeedToBe.any(axis=0)
    columnNamesWithMatch = seriesOfColumnsWithTrueIfAny[seriesOfColumnsWithTrueIfAny].index.values
    cuttedDataframeWithTrueInPlacesWhereTheValueNeedToBe = cuttedDataframeWithTrueInPlacesWhereTheValueNeedToBe.loc[:, columnNamesWithMatch]

    for currColumnName in columnNamesWithMatch:
        matchColumn = getCurrColumnFromColumnNameInAllMzData(currColumnName)
        x = cuttedDataframeWithTrueInPlacesWhereTheValueNeedToBe[currColumnName]
        for row, value in x.items():
            if(value):
                matchedMZDataFrame.iloc[row, matchColumn] = currNumber

        # seriesWithTrueInPlacesWhereTheValueNeedToBe = cuttedDataframeWithTrueInPlacesWhereTheValueNeedToBe[currColumnName]
        # listOfRowsAny = seriesWithTrueInPlacesWhereTheValueNeedToBe.index.values

        # matchedMZDataFrame.loc[:, matchColumn] = matchedMZDataFrame.loc[seriesWithTrueInPlacesWhereTheValueNeedToBe, matchColumn].\
        #                                                                         replace(np.nan, currNumber)

    # for currColumnNameInAllMzData in dataframeWithTheRelevantRowsForMatch.iloc[:, column + 1:]:
    #
    #     matchedRowsInCurrColumnIndex = dataframeWithTheRelevantRowsForMatch.loc[
    #                                             (dataframeWithTheRelevantRowsForMatch[currColumnNameInAllMzData] >= 325) &
    #                                             (dataframeWithTheRelevantRowsForMatch[currColumnNameInAllMzData] <= 330)].index
    #
    #     if(not matchedRowsInCurrColumnIndex.empty):
    #         matchColumn = getCurrColumnFromColumnNameInAllMzData(currColumnNameInAllMzData)
    #         matchRow = matchedRowsInCurrColumnIndex.item()
    #         matchedMZDataFrame.iloc[matchRow, matchColumn] = currNumber


def getDataFrameFilledWithMatchedMZ(allMZData):

    # initialize the matchedMZDataFrame
    numberOfRows, numberOfColumns = allMZData.shape
    matchedMZDataFrame = pd.DataFrame(index=range(numberOfRows),
                                      columns=range(numberOfColumns))

    # matchedMZDataFrame[0] = np.arange(number_of_rows)
    # x = matchedMZDataFrame.dtypes


    # initialize the number need for iterating
    currNumber = 0

    # iteration over the df
    for column in matchedMZDataFrame:
        currMatchedMZDataFrameColumn = matchedMZDataFrame[column]
        for row, value in currMatchedMZDataFrameColumn.items():
            print("column: " + str(column) + " row: " + str(row))
            if pd.isna(value):
                fillMatchedMZDataFrame(allMZData, matchedMZDataFrame, row, column, currNumber)
                currNumber += 1

    return matchedMZDataFrame


def main():
    # allData = getDataFrameWithAllDataFramesTogether()
    scriptDirPath = os.path.dirname(__file__)
    dataDirPath = os.path.join(scriptDirPath, "data")

    exists = os.path.isfile(MZFileName)
    if not exists:
        allMZData = getDataFrameWithAllMZDataFramesTogether(dataDirPath)
        allMZData.to_excel(MZFileName)

    allMZData = pd.read_excel(MZFileName, index_col=0)

    if TO_CUT:
        allMZData = allMZData.iloc[:MAX_ROW, :MAX_COLUMN]

    matchedMZ = getDataFrameFilledWithMatchedMZ(allMZData)
    matchedMZ.to_excel(matchedMZFileName)


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

