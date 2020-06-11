# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 16:41:30 2020

@author: Lucas Viegas
"""

import SerialPort
import tkinter as tk


class SerialDialog(tk.simpledialog.Dialog):
    def __init__(self, master=None, title='None', callback=None):
        self.comsettings = {
            'port': '',
            'baudrate': '9600',
            'parity': 'Nenhuma',     # None, Even, Odd
            'stopbits': 1
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
        ports = SerialPort.GetPortsList()
        if (len(ports) > 0):
            serialTemp = SerialPort.SerialPort()
            self.port = self.createOptionMenu('Porta', ports)
            self.bauRate = self.createOptionMenu(
                'Baud', serialTemp.getBaudRates(), 3)
            self.parity = self.createOptionMenu(
                'Paridade', ['Nenhuma', 'Ímpar', 'Par'])
            self.stopBits = self.createOptionMenu(
                'Bits de parada', serialTemp.getStopBits())

    def apply(self):
        self.comsettings['port'] = self.port.get()
        if self.callback: self.callback(self.comsettings)


