# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import SerialPort
import tkinter as tk
from tkinter import filedialog

# Parte do projeto
from CurveWindow import CurveWindow    
from SerialDialog import SerialDialog

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
        
        # Curva
        self.curve = CurveWindow(self)
        self.curve.grid()
        self.serialPort = SerialPort.SerialPort()

    def onComSettings(self, comsettings):
        parity = 'N'
        if comsettings['parity'] == 'Ímpar':
            parity = 'O'
        elif comsettings['parity'] == 'Par':
            parity = 'E'

        if self.serialPort.isOpen():
            self.serialPort.close()
        self.serialPort.begin(port=comsettings['port'],
                              baudrate=comsettings['baudrate'],
                              parity=parity,
                              stopbits=comsettings['stopbits'])
        
    def startCapture(self):
        SerialDialog(self, title='Configurações de captura', callback=self.onComSettings)
        if self.serialPort.isOpen():
            self.master.after(100, self.logLoop)
        
    def logLoop(self):
        if self.serialPort.isOpen():
            if self.serialPort.available() > 1:
                valor = self.serialPort.readUint16()
                print(valor)
        else:
            return
        self.master.after(100, self.logLoop)

    def openFile(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Arquivos de texto", ".txt")])
        if filename:
            pass
  
root = tk.Tk()
root.option_add('*tearOff', False)
app = MainFrame(master=root)
app.mainloop()