# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 16:41:30 2020

@author: Lucas Viegas
"""

import serial
import tkinter as tk


class SerialDialog(tk.simpledialog.Dialog):
    def __init__(self, master):
        super().__init__(master)

    def body(self, master):
        self.variable = tk.StringVar(self)
        self.variable.set('teste1')
        self.options = tk.OptionMenu(self, self.variable, 'teste1', 'teste2')
        self.options.pack()

        return self.options


