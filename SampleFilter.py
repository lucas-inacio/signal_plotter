class BaseFilter():
    def __init__(self):
        pass

    def filter(self, x, y):
        xOut = []
        yOut = []
        for i in range(len(x)):
            if self.validate(x[i], y[i]):
                xOut.append(x[i])
                yOut.append(y[i])
        if len(xOut) > 0:
            return [xOut, yOut]
        else:
            return None

    def validate(self, x, y):
        return True

class SampleFilter(BaseFilter):
    def __init__(self, index, mod):
        self.index = index
        self.mod = mod

    def validate(self, x, y):
        if x % (self.mod + 1) == self.index:
            return True
        return False

    def setIndex(self, index):
        self.index = index

    def setMod(self, mod):
        self.mod = mod

    def filter(self, x, y):
        xOut = []
        yOut = []
        for i in range(len(x)):
            if self.validate(x[i], y[i]):
                xOut.append(x[i] // self.mod)
                yOut.append(y[i])
        if len(xOut) > 0:
            return [xOut, yOut]
        else:
            return None