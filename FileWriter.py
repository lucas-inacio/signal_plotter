import csv
import queue
import threading


class FileWriter(threading.Thread):
    def __init__(self, file, dataQueue):
        super().__init__()
        self.file = file
        self.writer = csv.writer(self.file)
        self.dataQueue = dataQueue

    def run(self):
        currentThread = threading.currentThread()
        while getattr(currentThread, 'shouldRun', True):
            try:
                data = self.dataQueue.get(timeout=0.1)
                self.writer.writerow(data)
            except queue.Empty:
                pass
        self.file.flush()
        self.file.close()
