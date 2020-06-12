# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from datetime import datetime
from pathvalidate import ValidationError, sanitize_filepath
import queue
from tkinter import filedialog
import tkinter as tk

# Parte do projeto
from CurveWindow import CurveWindow  
from FileWriter import FileWriter  
from SerialDialog import SerialDialog
import SerialPort

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
        menu_file.add_command(label='Iniciar captura', command=self.startCapture)

        # Aquisição
        self.serialPort = SerialPort.SerialPort()
        self.lastTime = 0
        self.timeElapsed = 0
        self.xdata = []
        self.ydata = []
        self.max = 1023
        self.fullScale = 5
        self.ratio = 1

        # Arquivo
        self.file = None
        self.fileName = None
        self.dataQueue = None

        # Curva
        self.curve = CurveWindow(self)
        self.curve.grid()
        self.curve.setXLabel('Tempo (s)')
        self.curve.setYLabel('Tensão (V)')
        self.curve.setXLimit(0, 10)
        self.curve.setYLimit(0, self.fullScale + 1)

    def updateCurve(self, y):
        now = datetime.now()
        delta = now - self.lastTime
        self.lastTime = now
        self.timeElapsed = self.timeElapsed + delta.total_seconds()
        left, right = self.curve.getXLimit()

        if self.timeElapsed > right:
            self.curve.setXLimit(self.timeElapsed - (right - left), self.timeElapsed)

        # Converte o valor amostrado
        valor = (self.fullScale / self.max) * y * self.ratio
        self.xdata.append(self.timeElapsed)
        self.ydata.append(valor)
        self.xdata = self.xdata[-60:]
        self.ydata = self.ydata[-60:]
        self.curve.setData(self.xdata, self.ydata)

    def onComSettings(self, comsettings, filePath):
        try:
            sanitize_filepath(filePath, platform='auto')
            if self.serialPort.isOpen():
                self.serialPort.close()
            self.serialPort.begin(port=comsettings['port'],
                                baudrate=comsettings['baudrate'],
                                bytesize=comsettings['bytesize'],
                                parity=comsettings['parity'],
                                stopbits=comsettings['stopbits'])
            self.filePath = filePath
        except ValidationError as e:
            tk.messagebox.showerror('Erro de arquivo', 'Caminho inválido')
        
    def startCapture(self):
        SerialDialog(self, title='Configurações de captura', callback=self.onComSettings)
        self.lastTime = datetime.now()
        self.timeElapsed = 0
        if self.serialPort.isOpen():
            self.master.after(100, self.getSample)

        self.file = open(self.filePath, 'w')
        self.dataQueue = queue.Queue()
        self.fileTask = FileWriter(self.file, self.dataQueue)
        self.fileTask.shouldRun = True
        self.fileTask.start()
    
    def closeFile(self):
        self.fileTask.shouldRun = False
        self.fileTask.join()
        
    def getSample(self):
        if self.serialPort.isOpen():
            if self.serialPort.available() > 1:
                valor = self.serialPort.readUint16()
                self.updateCurve(valor)
            self.master.after(100, self.getSample)

    def openFile(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Arquivos de texto", ".txt")])
        if filename:
            pass

def main():
    root = tk.Tk()
    root.option_add('*tearOff', False)
    app = MainFrame(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()