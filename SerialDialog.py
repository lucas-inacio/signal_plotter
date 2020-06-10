# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 16:41:30 2020

@author: Lucas Viegas
"""

from serial.tools import list_ports
import serial
import tkinter as tk


class SerialDialog(tk.simpledialog.Dialog):
    def __init__(self, master):
        super().__init__(master)

    def body(self, master):
        ports = serial.tools.list_ports.comports()
        if (len(ports) > 0):
            self.variable = tk.StringVar(self)
            self.variable.set(ports[0].device)

            self.ports_list = []
            for i in range(0, len(ports)):
                self.ports_list.append(ports[i].device)

            self.options = tk.OptionMenu(self, self.variable, *self.ports_list)
            self.options.pack()
            return self.options
        else:
            self.label = tk.Label(self, text='Nenhuma porta disponível')
            self.label.pack()
            return self.label

    def show(self):
        self.wait_window()
        return 
        pass


