from CurveWindow import CurveWindow
from SampleFilter import BaseFilter


class SamplingWindow(CurveWindow):
    def __init__(self, master, maxSamples=60, filter=None):
        super().__init__(master)
        self.maxSamples = maxSamples
        self.xdata = []
        self.ydata = []
        if filter:
            self.filter = filter
        else:
            self.filter = BaseFilter()

    def addSamples(self, x, y):
        data = self.filter.filter(x, y)
        if data:
            left, right = self.getXLimit()
            if data[0][-1] > right:
                self.setXLimit(data[0][-1] - (right - left), data[0][-1])

            bottom, top = self.getYLimit()
            if data[1][-1] > top or data[1][-1] < bottom:
                yOffset = (top - bottom) / 2
                self.setYLimit(data[1][-1] - yOffset, data[1][-1] + yOffset)
            self.xdata.extend(data[0])
            self.ydata.extend(data[1])
            self.xdata = self.xdata[-self.maxSamples:]
            self.ydata = self.ydata[-self.maxSamples:]
            super().setData(self.xdata, self.ydata)


    def addSample(self, x, y):
        left, right = self.getXLimit()
        if x > right:
            self.setXLimit(x - (right - left), x)

        self.xdata.append(x)
        self.ydata.append(y)
        self.xdata = self.xdata[-self.maxSamples:]
        self.ydata = self.ydata[-self.maxSamples:]
        self.setData(self.xdata, self.ydata)

    def setData(self, x, y):
        data = self.filter.filter(x, y)
        if data:
            self.xdata = x[:len(data[0])]
            self.ydata = data[1]
        else:
            self.xdata = []
            self.ydata = []
        super().setData(self.xdata, self.ydata)

    def restart(self):
        self.xdata = []
        self.ydata = []
        left, right = self.getXLimit()
        self.setXLimit(0, right - left)
        bottom, top = self.getYLimit()
        self.setYLimit(0, top - bottom)
        self.setData(self.xdata, self.ydata)

    def clear(self):
        self.xdata = []
        self.ydata = []
        super().setData(self.xdata, self.ydata)