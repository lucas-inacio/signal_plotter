import serial
from serial.tools import list_ports


class SerialPort:
    def __init__(self):
        self.serialPort = serial.Serial()

    def available(self):
        return self.serialPort.in_waiting

    def begin(self, port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=None):
        if not self.serialPort.is_open:
            self.serialPort.baudrate = baudrate
            self.serialPort.bytesize = bytesize
            self.serialPort.parity = parity
            self.serialPort.stopbits = stopbits
            self.serialPort.timeout = timeout
            self.serialPort.port = port
            self.serialPort.open()

    def close(self):
        if self.serialPort.is_open:
            self.serialPort.close()

    def getBaudRates(self):
        return self.serialPort.BAUDRATES

    def getByteSizes(self):
        return self.serialPort.BYTESIZES

    def getParities(self):
        return self.serialPort.PARITIES

    def getStopBits(self):
        return self.serialPort.STOPBITS

    def isOpen(self):
        return self.serialPort.is_open

    def read(self, count=1):
        return self.serialPort.read(count)
    
    def readInt16(self, byteorder='little'):
        data = self.serialPort.read(2)
        return int.from_bytes(data, byteorder, signed=True)

    def readUint16(self, byteorder='little'):
        data = self.serialPort.read(2)
        return int.from_bytes(data, byteorder, signed=False)

    def write(self, data):
        return self.serialPort.write(data)

    def writeInt16(self, number, byteorder='little'):
        return self.serialPort.write((number).to_bytes(2, byteorder, signed=True))

    def writeUint16(self, number, byteorder='little'):
        return self.serialPort.write((number).to_bytes(2, byteorder, signed=False))

    def flush(self):
        self.serialPort.flush()


def GetPortsList():
    ports = list_ports.comports()
    ports_list = []
    for i in range(0, len(ports)):
        ports_list.append(ports[i].device)
    return ports_list