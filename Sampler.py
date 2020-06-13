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

    def reset(self):
        self.lastTimestamp = datetime.now()
        self.timeElaspsed = 0

    def getSample(self):
        if self.sampleSource.available() > 1:
            now = datetime.now()
            delta = now - self.lastTimestamp
            self.lastTimestamp = now
            self.timeElaspsed = self.timeElaspsed + delta.total_seconds()
            valor = self.sampleSource.readUint16() * (self.fullScale / self.maxAD) * self.ratio
            return (self.timeElaspsed, valor)