import lib.StringFiller as StringFiller
import lib.TimeFormatter as TimeFormatter
import json

def groupRowDataByDateValue(rowDataList):
    newRowDataList = []
    currentRowData = RowData("", 0, 0)

    for rowData in rowDataList:
        if currentRowData.dateValue == "":
            currentRowData = rowData
            continue

        if currentRowData.dateValue != rowData.dateValue:
            newRowDataList.append(currentRowData)
            currentRowData = rowData
            continue

        currentRowData = currentRowData.merge(rowData)

    newRowDataList.append(currentRowData)
    return newRowDataList

class RowData:
    def __init__(self, dateValue, breakTime, totalTime):
        self.dateValue = dateValue
        self.breakTime = breakTime
        self.totalTime = totalTime

    def toJson(self):
        return json.dumps({"dataValue":self.dateValue, "totalTime":self.totalTime}, indent=4)

    def toString(self):
        return "dataValue:" + self.dateValue + ",totalTime:" + str(self.totalTime)

    def merge(self, rowData):
        return RowData(self.dateValue, self.breakTime+rowData.breakTime, self.totalTime+rowData.totalTime)

class Length:
    maxLengthDateColumn = 0
    maxLengthBreakTime = len("Break Time")
    maxLengthTotalTime = len("Total Time")

class TablePrinter:
    def __init__(self, firstColumnName):
        self.maxLength = Length()
        self.firstColumnName = firstColumnName
        self.maxLengthOfFirstColumn = len(firstColumnName)

    def printTable(self, rowDataList):
        self.maxLength = Length()
        self.maxLength.maxLengthDateColumn = len(self.firstColumnName)

        totalRowData = RowData("Total", 0, 0)

        for rowData in rowDataList:
            currentLengthOfFirstColumn = len(rowData.dateValue)
            if currentLengthOfFirstColumn > self.maxLength.maxLengthDateColumn:
                self.maxLength.maxLengthDateColumn = currentLengthOfFirstColumn

            currentLengthOfBreakTime = len(str(rowData.breakTime))
            if currentLengthOfBreakTime > self.maxLength.maxLengthBreakTime:
                self.maxLength.maxLengthBreakTime = currentLengthOfBreakTime

            totalRowData.totalTime += rowData.totalTime

        breakTimeStringLength = len(str(totalRowData.breakTime))
        if breakTimeStringLength > self.maxLength.maxLengthBreakTime:
            self.maxLength.maxLengthBreakTime = breakTimeStringLength

        self.printHeadline()
        totalBreakTime = 0
        for rowData in rowDataList:
            totalBreakTime += rowData.breakTime
            self.printRow(rowData, 0)
        self.printTotalLine(totalRowData, totalBreakTime)

    def printHeadline(self):
        firstColumnNameToDisplay = StringFiller.fillString(self.firstColumnName, self.maxLength.maxLengthDateColumn+2, " ")
        firstColumnNameDelimiterFiller = StringFiller.fillString("", self.maxLength.maxLengthDateColumn+2, "-")

        print("+" + firstColumnNameDelimiterFiller + "-----------------------------------------+")
        print("|" + firstColumnNameToDisplay + "| Tracked Time | Break Time | Total Time |")
        print("+" + firstColumnNameDelimiterFiller + "-----------------------------------------+")

    def printTotalLine(self, rowData, totalBreakTime):
        firstColumnName = "Total"
        firstColumnNameToDisplay = StringFiller.fillString(firstColumnName, self.maxLength.maxLengthDateColumn+2, " ")
        firstColumnNameDelimiterFiller = StringFiller.fillString("", self.maxLength.maxLengthDateColumn+2, "-")

        print("+" + firstColumnNameDelimiterFiller + "-----------------------------------------+")
        self.printRow(rowData, totalBreakTime)
        print("+" + firstColumnNameDelimiterFiller + "-----------------------------------------+")

    def printRow(self, rowData, breakTime):
        firstColumnName = ""
        firstColumnNameToDisplay = StringFiller.fillString(rowData.dateValue, self.maxLength.maxLengthDateColumn+2, " ")

        formattedTotalTime = TimeFormatter.formatMinutesInHours(rowData.totalTime)
        totalTimeToDisplay = StringFiller.fillString(formattedTotalTime, self.maxLength.maxLengthTotalTime+2, " ")

        # custom breakTime
        if breakTime == 0:
            breakTime = rowData.breakTime

        if breakTime > 60:
            formattedBreakTime = TimeFormatter.formatMinutesInHours(breakTime)
        else:
            formattedBreakTime = TimeFormatter.formatMinutes(breakTime)
        breakTimeToDisplay = StringFiller.fillString(formattedBreakTime, self.maxLength.maxLengthTotalTime+2, " ")

        trackedTime = rowData.totalTime - breakTime
        formattedTrackedTime = TimeFormatter.formatMinutesInHours(trackedTime)
        trackedTimeToDisplay = StringFiller.fillString(formattedTrackedTime, 14, " ")

        print("|" + firstColumnNameToDisplay + "|" + trackedTimeToDisplay + "|" + breakTimeToDisplay + "|" + totalTimeToDisplay + "|")
