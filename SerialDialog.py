# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 16:41:30 2020

@author: Lucas Viegas
"""

from serial.tools import list_ports
import serial
import tkinter as tk


class SerialDialog(tk.simpledialog.Dialog):
    def __init__(self, master=None, title='None', callback=None):
        self.comsettings = {
            'port': '',
            'baudRate': 9600,
            'parity': 'N',     # None, Even, Odd
            'stopBits': 1
        }
        self.callback = callback
        tk.simpledialog.Dialog.__init__(self, master, title)

    def createOptionMenu(self, label, *options):
        variable = tk.StringVar(self)
        variable.set(options[0])
        optionMenu = tk.OptionMenu(self, variable, *options)
        optionMenu.pack()
        return variable

    def body(self, master):
        ports = serial.tools.list_ports.comports()
        if (len(ports) > 0):
            ports_list = []
            for i in range(0, len(ports)):
                ports_list.append(ports[i].device)
            self.port = self.createOptionMenu('Porta', *ports_list)

    
    def apply(self):
        self.comsettings['port'] = self.port.get()
        if self.callback: self.callback(self.comsettings)
        print(self.comsettings)


