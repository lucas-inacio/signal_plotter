# -*- coding: utf-8 -*-
"""
Created on Sun May 24 20:30:37 2020

@author: lucas
"""

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import tkinter as tk

import numpy as np


class CurveWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # Curva
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.autoscale(enable=True)
        self.data, = ax.plot([], [])
        
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid()
        
        # Coordenadas iniciais para arrastar
        self.dragX = 0
        self.dragY = 0
        self.dragging = False
        self.modKey = False # Shift key
        
        self.canvas.mpl_connect("button_press_event", self.eventHandler)
        self.canvas.mpl_connect("button_release_event", self.eventHandler)
        self.canvas.mpl_connect("motion_notify_event", self.eventHandler)
        self.canvas.mpl_connect("scroll_event", self.eventHandler)
        self.canvas.mpl_connect("key_press_event", self.handleKey)
        self.canvas.mpl_connect("key_release_event", self.handleKey)
        self.canvas.mpl_connect("figure_enter_event", self.eventHandler)

    def getData(self):
        return (self.data.get_xdata(), self.data.get_ydata())
        
    def setData(self, x, y):
        self.data.set_xdata(x)
        self.data.set_ydata(y)
        self.canvas.draw()
        
    def setXLabel(self, label):
        self.data.axes.set_xlabel(label)
        
    def setYLabel(self, label):
        self.data.axes.set_ylabel(label)
        
    def getXLimit(self):
        return self.data.axes.get_xlim()
    
    def getYLimit(self):
        return self.data.axes.get_ylim()
        
    def setXLimit(self, start, stop):
        self.data.axes.set_xlim(left=start, right=stop)
        self.canvas.draw()
        
    def setYLimit(self, start, stop):
        self.data.axes.set_ylim(bottom=start, top=stop)
        self.canvas.draw()
        
    def handleZoom(self, event):
        start, stop = self.getYLimit() if self.modKey else self.getXLimit()
        delta = event.step * (np.abs(stop - start) / 100)
        start += delta
        stop -= delta
        
        if self.modKey:
            self.setYLimit(start, stop)
        else:
            self.setXLimit(start, stop)
        self.canvas.draw()
        
    def handleDragging(self, event):
        dx = (event.x - self.dragX)
        self.dragX += dx
        left, right = self.getXLimit()
        scale = 200.0 / np.abs(right - left)
        left -= dx / scale
        right -= dx / scale
        self.setXLimit(left, right)
        
        dy = (event.y - self.dragY)
        self.dragY += dy
        bottom, top = self.getYLimit()
        scale = 200.0 / np.abs(top - bottom)
        bottom -= dy / scale
        top -= dy / scale
        self.setYLimit(bottom, top)
        
        self.canvas.draw()
        
    def handleKey(self, event):
        if event.key == "shift":
            if event.name == "key_press_event":
                self.modKey = True
            elif event.name == "key_release_event":
                self.modKey = False
        
    def eventHandler(self, event):
        # Zoom horizontal/vertical
        if event.name == "scroll_event":
            self.handleZoom(event)
        # Arrasta o gráfico
        elif self.dragging:
            if event.name == "motion_notify_event":
                self.handleDragging(event)
            elif event.name == "button_release_event":
                self.dragging = False
                self.canvas.draw()
        elif event.name == "button_press_event":
            self.dragX = event.x
            self.dragY = event.y
            self.dragging = True
        # É necessário definir o foco do teclado quando o cursor entrar em
        # um gráfico
        if event.name == "figure_enter_event":
            self.canvas.get_tk_widget().focus_set()