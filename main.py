from tkinter import filedialog
import tkinter as tk

from DataLogger import CSVLogger, XLSLogger
from LogReader import CSVReader, XLSReader
from Sampler import Sampler
from SampleFilter import SampleFilter
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
        self.uiState = 'main' # Possíveis estados: main, acqu, file e stop
        
        self.master.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.buildMenu()
        self.setMenuStateMain()

        # Aquisição
        self.serialPort = SerialPort.SerialPort()
        self.sampler = Sampler(self.serialPort)

        # Arquivo
        self.fileTask = None
        self.file = None
        self.filePath = ''
        self.fileTypes = [('CSV', '.csv'), ('Excel (1995 - 2003)', '.xls')]

        # Curva
        self.filter = SampleFilter(index=1, mod=12)
        self.curve = SamplingWindow(self, filter=self.filter)
        self.curve.grid()
        self.curve.setXLabel('Índice da Amostra')
        self.curve.setYLabel('Tensão (V)')
        self.curve.setXLimit(0, 24)
        self.curve.setYLimit(0, 6)

    def loadBatteryFrom(self, filepath):
        try:
            if filepath and filepath.endswith('.csv'):
                reader = CSVReader(filepath)
            elif filepath:
                reader = XLSReader(filepath)
            else:
                return False

            index = self.currentBattery
            data = reader.read()
            if data:
                x = data[0]
                y = data[1]
                self.filter.setIndex(index)
                self.curve.restart()
                self.curve.setData(x, y)
                return True
        except xlrd.XLRDError:
            pass

        tk.messagebox.showerror(message='Arquivo incompatível')
        return False

    def onBatteryChange(self, variable, index, mode):
        self.currentBattery = self.batterySelector.get()
        if self.uiState == 'file':
            self.loadBatteryFrom(self.filePath)
        elif self.uiState == 'acqu':
            self.filter.setIndex(self.batterySelector.get())
            self.curve.clear()
        elif self.uiState == 'stop':
            pass

    def updateCurve(self, x, y):
        self.curve.addSamples(x, y)
        self.fileTask.write([x, y])

    def startCapture(self, comsettings, filePath):
        self.stopCapture()
        # Abre arquivo e inicia thread para escrita
        self.filePath = filePath
        if filePath.endswith('.xls'):
            self.file = XLSLogger(self.filePath)
        else:
            self.file = CSVLogger(self.filePath)
        self.fileTask = FileWriter(self.file)
        self.fileTask.start()

        self.sampler.begin(comsettings)
        self.startLoop()

        # Reinicia gráfico
        self.curve.restart()
        self.setMenuStateAcqu()
        
    def startComDialog(self):
        SerialDialog(
            self, title='Configurações de captura', 
            callback=self.startCapture,
            filetypes=self.fileTypes)

    def stopCapture(self):
        if self.serialPort.isOpen():
            self.sampler.sendStop()
            self.sampler.reset()
            self.serialPort.close()
        self.closeFile()
        self.setMenuStateStop()
    
    def closeFile(self):
        if self.fileTask:
            self.fileTask.join()
            self.fileTask = None
        if self.file:
            self.file.close()
            self.file = None
        
    def closeWindow(self):
        self.stopCapture()
        self.master.destroy()

    def startLoop(self):
        if self.serialPort.isOpen():
            if not self.sampler.isReady():
                self.sampler.sendStart()
                self.master.after(100, self.startLoop)
            else:
                self.master.after(100, self.sampleLoop)

    def sampleLoop(self): 
        if self.serialPort.isOpen():
            sample = self.sampler.getSamples()
            if sample : self.updateCurve(sample[0], sample[1])
            self.master.after(100, self.sampleLoop)

    def openFile(self):
        filename = filedialog.askopenfilename(filetypes=self.fileTypes)
        if self.loadBatteryFrom(filename):
            self.setMenuStateFile()
            self.filePath = filename

    def buildMenu(self):
        # Menus
        self.menubar = tk.Menu(self)
        self.master['menu'] = self.menubar
        self.menu_file = tk.Menu(self.menubar)
        # Menu Arquivo
        self.menubar.add_cascade(menu=self.menu_file, label='Arquivo')
        self.menu_file.add_command(label='Abrir', command=self.openFile)
        self.menu_file.add_command(label='Iniciar captura',
                                   command=self.startComDialog)
        self.menu_file.add_command(label='Parar captura',
                                   command=self.stopCapture)
        # Menu Bateria
        self.currentBattery = 1
        self.batterySelector = tk.IntVar()
        self.batterySelector.set(1)
        self.callbackName = self.batterySelector.trace_add(
            'write', self.onBatteryChange)
        self.menu_batt = tk.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_batt, label='Bateria')
        for i in range(1, 13):
            self.menu_batt.add_radiobutton(label=str(i),
                                           variable=self.batterySelector)

    def setMenuStateMain(self):
        self.uiState = 'main'
        self.menubar.entryconfig('Bateria', state=tk.DISABLED)
        self.menu_file.entryconfig('Abrir', state=tk.NORMAL)
        self.menu_file.entryconfig('Iniciar captura', state=tk.NORMAL)
        self.menu_file.entryconfig('Parar captura', state=tk.DISABLED)

    def setMenuStateFile(self):
        self.uiState = 'file'
        self.menubar.entryconfig('Bateria', state=tk.NORMAL)
        self.menu_file.entryconfig('Abrir', state=tk.NORMAL)
        self.menu_file.entryconfig('Iniciar captura', state=tk.NORMAL)
        self.menu_file.entryconfig('Parar captura', state=tk.DISABLED)

    def setMenuStateAcqu(self):
        self.uiState = 'acqu'
        self.menubar.entryconfig('Bateria', state=tk.NORMAL)
        self.menu_file.entryconfig('Abrir', state=tk.DISABLED)
        self.menu_file.entryconfig('Iniciar captura', state=tk.DISABLED)
        self.menu_file.entryconfig('Parar captura', state=tk.NORMAL)

    def setMenuStateStop(self):
        self.uiState = 'stop'
        self.menubar.entryconfig('Bateria', state=tk.NORMAL)
        self.menu_file.entryconfig('Abrir', state=tk.NORMAL)
        self.menu_file.entryconfig('Iniciar captura', state=tk.NORMAL)
        self.menu_file.entryconfig('Parar captura', state=tk.DISABLED)


def main():
    root = tk.Tk()
    root.option_add('*tearOff', False) # Impede que o menu seja destacado da janela principal
    app = MainFrame(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()