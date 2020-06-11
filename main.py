# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import asyncio
import random
import serial
import tkinter as tk
from tkinter import filedialog
import numpy as np
import time

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
        self.serialPort = serial.Serial()

    def onComSettings(self, comsettings):
        parity = serial.PARITY_EVEN
        if comsettings['parity'] == 'Nenhuma':
            parity = serial.PARITY_NONE
        elif comsettings['parity'] == 'Ímpar':
            parity = serial.PARITY_ODD
        else:
            parity = serial.PARITY_EVEN

        if self.serialPort.is_open:
            self.serialPort.close()
        self.serialPort.port = comsettings['port']
        self.serialPort.baudrate = int(comsettings['baudrate'])
        self.serialPort.parity = parity
        self.serialPort.stopbits = int(comsettings['stopbits'])
        self.serialPort.timeout = 0.01
        self.serialPort.open()
        
    def startCapture(self):
        SerialDialog(self, title='Configurações de captura', callback=self.onComSettings)
        if self.serialPort.is_open:
            self.master.after(100, self.logLoop)
        
    def logLoop(self):
        if self.serialPort.is_open:
            bytes = self.serialPort.read() # Pode fornecer o número de bytes como argumento
            if bytes:
                print(bytes)
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