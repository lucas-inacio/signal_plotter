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
        data = []
        for i in self.reader:
            x = float(i[0])
            y = float(i[1])
            data.append([x, y])
        return data

class XLSReader(LogReader):
    def __init__(self, filePath):
        super().__init__(filePath)
        self.book = self.file

    def open(self):
        return xlrd.open_workbook(self.filePath)

    def read(self):
        data = []
        sheet = self.book.sheet_by_index(0)
        for index in range(0, (sheet.ncols - 1) * (sheet.nrows - 1)):
            row = (index // (sheet.ncols - 1)) * 2 + 1
            col = (index % (sheet.ncols - 1)) + 1
            y = sheet.cell(row, col).value
            x = sheet.cell(row + 1, col).value
            if y == '' or x == '': break
            data.append([float(x), float(y)])
        return data

    def close(self):
        pass

    