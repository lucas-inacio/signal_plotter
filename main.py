from tkinter import filedialog
import tkinter as tk

# Parte do projeto
from DataLogger import CSVLogger, XLSLogger
from LogReader import CSVReader, XLSReader
from Sampler import Sampler
from SamplingWindow import SamplingWindow
from FileWriter import FileWriter  
from SerialDialog import SerialDialog
import SerialPort
import xlrd

class MainFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        
        self.menubar = tk.Menu(self)
        self.master['menu'] = self.menubar
        menu_file = tk.Menu(self.menubar)
        self.menubar.add_cascade(menu=menu_file, label='Arquivo')
        menu_file.add_command(label='Abrir', command=self.openFile)
        menu_file.add_command(label='Iniciar captura', command=self.startComDialog)
        menu_file.add_command(label='Parar captura', command=self.stopCapture)
        self.master.protocol("WM_DELETE_WINDOW", self.closeWindow)

        # Aquisição
        self.serialPort = SerialPort.SerialPort()
        self.sampler = Sampler(self.serialPort)

        # Arquivo
        self.fileTask = None
        self.file = None
        self.filePath = ''
        self.fileTypes = [('CSV', '.csv'), ('Excel (1995 - 2003)', '.xls')]

        # Curva
        self.curve = SamplingWindow(self)
        self.curve.grid()
        self.curve.setXLabel('Índice da Amostra')
        self.curve.setYLabel('Tensão (V)')
        self.curve.setXLimit(0, 24)
        self.curve.setYLimit(0, 6)

    def updateCurve(self, x, y):
        self.curve.addSamples(x, y)
        self.fileTask.write([x, y])

    def startCapture(self, comsettings, filePath):
        if self.serialPort.isOpen():
            self.serialPort.close()
        # Abre arquivo e inicia thread para escrita
        self.filePath = filePath
        if filePath.endswith('.xls'):
            self.file = XLSLogger(self.filePath)
        else:
            self.file = CSVLogger(self.filePath)
        self.fileTask = FileWriter(self.file)
        self.fileTask.start()

        self.serialPort.begin(port=comsettings['port'],
                              baudrate=comsettings['baudrate'],
                              bytesize=comsettings['bytesize'],
                              parity=comsettings['parity'],
                              stopbits=comsettings['stopbits'])
        self.sampler.reset()
        self.sampleLoop()

        # Reinicia gráfico
        self.curve.restart()
        
    def startComDialog(self):
        SerialDialog(
            self, title='Configurações de captura', 
            callback=self.startCapture,
            filetypes=self.fileTypes)

    def stopCapture(self):
        if self.serialPort.isOpen():
            self.serialPort.close()
        self.closeFile()
    
    def closeFile(self):
        if self.fileTask:
            self.fileTask.join()
            self.fileTask = None
        if self.file:
            self.file.close()
            self.file = None
        
    def closeWindow(self):
        self.closeFile()
        self.master.destroy()

    def sampleLoop(self):
        if self.serialPort.isOpen():
            sample = self.sampler.getSamples()
            if sample : self.updateCurve(sample[0], sample[1])
            self.master.after(100, self.sampleLoop)

    def openFile(self):
        filename = filedialog.askopenfilename(filetypes=self.fileTypes)
        reader = None

        try:
            if filename and filename.endswith('.csv'):
                reader = CSVReader(filename)
            elif filename:
                reader = XLSReader(filename)
            else:
                return
            self.stopCapture()
            data = reader.read()
        except xlrd.XLRDError:
            data = None

        if data:
            x = data[0]
            y = data[1]
            self.curve.restart()
            self.curve.setData(x, y)
        else:
            tk.messagebox.showerror(message='Arquivo incompatível')

def main():
    root = tk.Tk()
    root.option_add('*tearOff', False) # Impede que o menu seja destacado da janela principal
    app = MainFrame(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()