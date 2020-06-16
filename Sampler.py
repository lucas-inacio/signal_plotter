from datetime import datetime
import queue


class Sampler:
    def __init__(self, sampleSource, bitResolution=10, fullScale=5, ratio=1):
        self.sampleSource = sampleSource
        self.maxAD = 2 ** bitResolution - 1
        self.fullScale = fullScale
        self.ratio = ratio
        self.lastTimestamp = None
        self.timeElaspsed = 0
        self.sampleCount = 0

    def getTimeElapsed(self):
        self.timeElaspsed

    def computeDelta(self):
        now = datetime.now()
        delta = now - self.lastTimestamp
        self.lastTimestamp = now
        self.timeElaspsed = self.timeElaspsed + delta.total_seconds()

    def reset(self):
        self.lastTimestamp = datetime.now()
        self.timeElaspsed = 0
        self.sampleCount = 0

    def getSamples(self):
        dataX = []
        dataY = []
        while self.sampleSource.available() > 1:
            valor = self.sampleSource.readUint16() * (self.fullScale / self.maxAD) * self.ratio
            dataX.append(self.sampleCount)
            dataY.append(valor)
            self.sampleCount = self.sampleCount + 1
        self.computeDelta()
        if len(dataX) > 0: return [dataX, dataY]
        else: return None