import csv
from xlwt import Workbook


class DataLogger():
    def __init__(self, filePath):
        self.filePath = filePath
        self.file = self.open()

    def open(self):
        return open(self.filePath, 'w')

    def write(self, data):
        self.file.write()

    def flush(self):
        self.file.flush()

    def close(self):
        self.file.close()

class CSVLogger(DataLogger):
    def __init__(self, filePath):
        super().__init__(filePath)
        self.writer = csv.writer(self.file)

    def open(self):
        file = open(self.filePath, 'w', newline='')
        return file

    def write(self, data):
        dataX = data[0]
        dataY = data[1]
        if len(dataX) != len(dataY): raise ValueError

        for index in range(0, len(dataX)):
            self.writer.writerow([dataX[index], dataY[index]])

    def flush(self):
        self.file.flush()

    def close(self):
        self.file.close()

class XLSLogger(DataLogger):
    def __init__(self, filePath, maxCols=12):
        super().__init__(filePath)
        self.book = Workbook(encoding='utf-8')
        self.amostras = self.book.add_sheet('Amostras')
        for col in range(0, maxCols):
            self.amostras.write(0, col + 1, 'Bateria ' + str(col + 1))
        self.sampleCount = 0
        self.maxCols = maxCols

    def open(self):
        file = open(self.filePath, 'wb')
        return file

    def write(self, data):
        dataX = data[0]
        dataY = data[1]
        if len(dataX) != len(dataY): raise ValueError

        for index in range(0, len(dataX)):
            col = self.sampleCount % self.maxCols + 1
            row = (self.sampleCount // self.maxCols) * 2 + 1
            if col == 1:
                self.amostras.write(row, 0, 'Medida')
                self.amostras.write(row + 1, 0, 'Horário')
            self.amostras.write(row, col, dataY[index])
            self.amostras.write(row + 1, col, dataX[index])
            self.sampleCount = self.sampleCount + 1

    def flush(self):
        self.book.save(self.file)
        self.file.flush()

    def close(self):
        self.file.close()