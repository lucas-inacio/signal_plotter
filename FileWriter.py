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
        while True:
            try:
                data = self.dataQueue.get(timeout=0.1)
                if data == None: break
                self.writer.writerow(data)
            except queue.Empty:
                pass
        self.file.flush()
