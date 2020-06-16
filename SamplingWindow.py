from CurveWindow import CurveWindow


class SamplingWindow(CurveWindow):
    def __init__(self, master, maxSamples=60):
        super().__init__(master)
        self.maxSamples = maxSamples
        self.xdata = []
        self.ydata = []

    def addSamples(self, x, y):
        left, right = self.getXLimit()
        if x[-1] > right:
            self.setXLimit(x[-1] - (right - left), x[-1])

        bottom, top = self.getYLimit()
        if y[-1] > top or y[-1] < bottom:
            yOffset = (top - bottom) / 2
            self.setYLimit(y[-1] - yOffset, y[-1] + yOffset)

        self.xdata.extend(x)
        self.ydata.extend(y)
        self.xdata = self.xdata[-self.maxSamples:]
        self.ydata = self.ydata[-self.maxSamples:]
        self.setData(self.xdata, self.ydata)


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
        self.xdata = x
        self.ydata = y
        super().setData(x, y)

    def restart(self):
        self.xdata = []
        self.ydata = []
        left, right = self.getXLimit()
        self.setXLimit(0, right - left)
        bottom, top = self.getYLimit()
        self.setYLimit(0, top - bottom)
        self.setData(self.xdata, self.ydata)