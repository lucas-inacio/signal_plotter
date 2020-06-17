import csv
import xlrd


class LogReader():
    def __init__(self, filePath):
        self.filePath = filePath
        self.file = self.open()

    def open(self):
        return open(self.filePath, 'r')

    def read(self):
        return self.file.read()

    def close(self):
        self.file.close()

class CSVReader(LogReader):
    def __init__(self, filePath):
        super().__init__(filePath)
        self.reader = csv.reader(self.file)

    def open(self):
        return open(self.filePath, 'r', newline='')

    def read(self):
        dataX = []
        dataY = []
        count = 0
        for i in self.reader:
            count = count + 1
            y = float(i[1])
            dataX.append(count)
            dataY.append(y)
        if len(dataX) > 0:
            return [dataX, dataY]
        else:
            return None

class XLSReader(LogReader):
    def __init__(self, filePath):
        super().__init__(filePath)
        self.book = self.file

    def open(self):
        return xlrd.open_workbook(self.filePath)

    def read(self):
        dataX = []
        dataY = []
        sheet = self.book.sheet_by_index(0)
        if sheet.ncols > 2 and sheet.nrows > 2:
            for index in range(0, (sheet.ncols - 1) * (sheet.nrows - 1)):
                row = (index // (sheet.ncols - 1)) + 1
                col = (index % (sheet.ncols - 1)) + 1
                y = sheet.cell(row, col).value
                x = index + 1
                if y == '' or x == '': break
                dataX.append(x)
                dataY.append(y)
        if len(dataX) > 0:
            return [dataX, dataY]
        else:
            return None

    def close(self):
        pass

    