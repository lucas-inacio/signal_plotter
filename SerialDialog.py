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
            'baudRate': '9600',
            'parity': 'Nenhuma',     # None, Even, Odd
            'stopBits': 1
        }
        self.callback = callback
        self.row = 0
        tk.simpledialog.Dialog.__init__(self, master, title)

    def createOptionMenu(self, label, options, default=0):
        variable = tk.StringVar(self)
        variable.set(options[default])
        desc = tk.Label(self.frame, text=label)
        desc.grid(row=self.row, column=0, padx=5)
        optionMenu = tk.OptionMenu(self.frame, variable, *options)
        optionMenu.grid(row=self.row, column=1, padx=5)

        self.row = self.row + 1
        return variable

    def body(self, master):
        self.frame = tk.Frame(self)
        self.frame.pack()
        ports = serial.tools.list_ports.comports()
        if (len(ports) > 0):
            ports_list = []
            for i in range(0, len(ports)):
                ports_list.append(ports[i].device)
            self.port = self.createOptionMenu('Porta', ports_list)

            bauds = [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]
            self.bauRate = self.createOptionMenu('Baud', bauds, 3)
            self.parity = self.createOptionMenu(
                'Paridade', ['Nenhuma', 'Ímpar', 'Par'])
            self.stopBits = self.createOptionMenu('Bits de parada', [1, 2])

    
    def apply(self):
        self.comsettings['port'] = self.port.get()
        if self.callback: self.callback(self.comsettings)


