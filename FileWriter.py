import csv
from datetime import datetime
import queue
import threading


class FileWriter(threading.Thread):
    def __init__(self, file, autoSaveTimeout=300):
        super().__init__()
        self.file = file
        self.writer = csv.writer(self.file)
        self.dataQueue = queue.Queue()
        self.lastTimestamp = 0
        self.autoSaveTimeout = autoSaveTimeout

    def run(self):
        self.lastTimestamp = datetime.now()
        while True:
            try:
                data = self.dataQueue.get(timeout=0.1)
                if data == None: break
                self.writer.writerow(data)
            except queue.Empty:
                pass
            # Aplica alterações no arquivo após autoSaveTimeout segundos
            now = datetime.now()
            delta = now - self.lastTimestamp
            if delta.total_seconds() > self.autoSaveTimeout:
                self.file.flush()
                self.lastTimestamp = now
        self.file.flush()

    def join(self):
        self.dataQueue.put(None)
        super().join()

    def write(self, data):
        self.dataQueue.put(data)
