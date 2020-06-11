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

async def getSample(lock):
    await asyncio.sleep(1)
    value = random.randint(0, 1023)
    return value

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

    def onComSettings(self, comsettings):
        print(comsettings)
        
    def startCapture(self):
        SerialDialog(self, title='Configurações de captura', callback=self.onComSettings)
        
    def logLoop(self):
        pass

    def openFile(selef):
        filename = filedialog.askopenfilename(
            filetypes=[("Arquivos de texto", ".txt")])
        if filename:
            pass
                    
        
root = tk.Tk()
root.option_add('*tearOff', False)
app = MainFrame(master=root)
app.mainloop()