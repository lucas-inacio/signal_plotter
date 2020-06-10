# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

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
        
        # Menu
        self.menuButton = tk.Menubutton(self, text="Arquivo")
        self.menuButton.grid(column=0, row=0)
        
        self.menuButton.menu = tk.Menu(self.menuButton)
        self.menuButton["menu"] = self.menuButton.menu
        self.menuButton.menu.add_command(label="Iniciar captura",
                                         command=self.logEvents)
        
        # Curva
        self.curve = CurveWindow(self)
        self.curve.grid()
        
    def logEvents(self):
        #filename = filedialog.askopenfilename(
        #    filetypes=[("Arquivos de áudio", ".wav")])
        #if filename:
        #    pass
        dialog = SerialDialog(self)
        
    def logLoop(self):
        pass

    def saveFile(selef):
        filename = filedialog.askopenfilename(
            filetypes=[("Arquivos de texto", ".txt")])
        if filename:
            pass
                    
        
root = tk.Tk()
app = MainFrame(master=root)
app.mainloop()