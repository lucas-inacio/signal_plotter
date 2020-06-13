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
from SamplingWindow import SamplingWindow
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
        menu_file.add_command(label='Parar captura', command=self.stopCapture)
        self.master.protocol("WM_DELETE_WINDOW", self.closeWindow)

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
        self.fileTask = None
        self.file = None
        self.fileName = None

        # Curva
        self.curve = SamplingWindow(self)
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

        # Converte o valor amostrado
        valor = (self.fullScale / self.max) * y * self.ratio
        self.curve.addSample(self.timeElapsed, valor)
        
        # Envia para o arquivo
        self.fileTask.write([self.timeElapsed, y])

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
        except ValidationError:
            tk.messagebox.showerror('Erro de arquivo', 'Caminho inválido')
        
    def startCapture(self):
        SerialDialog(self, title='Configurações de captura', callback=self.onComSettings)
        if self.filePath == '':
            tk.messagebox.showerror('Erro de arquivo', 'Escolha um nome para o arquivo')
            return
            
        # Inicia aquisição
        self.lastTime = datetime.now()
        self.timeElapsed = 0
        if self.serialPort.isOpen():
            self.master.after(100, self.getSample)

        # Abre arquivo e inicia thread para escrita
        self.file = open(self.filePath, 'a', newline='')
        self.fileTask = FileWriter(self.file)
        self.fileTask.start()

        # Reinicia gráfico
        self.curve.restart()

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