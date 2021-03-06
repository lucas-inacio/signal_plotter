import os
from pathvalidate import ValidationError, validate_filepath
import serial
import SerialPort
import tkinter as tk


class SerialDialog(tk.simpledialog.Dialog):
    def __init__(self, master=None, title='None', callback=None, filetypes=None):
        self.fileTypes = filetypes
        self.comsettings = {
            'port': '',
            'baudrate': 9600,
            'bytesize': 8,
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
            self.baudrate = self.createOptionMenu(
                'Baud', serialTemp.getBaudRates(), 12)
            self.bytesize = self.createOptionMenu(
                'Byte size', serialTemp.getByteSizes(), 3)
            self.parity = self.createOptionMenu(
                'Paridade', ['Nenhuma', 'Ímpar', 'Par'])
            self.stopbits = self.createOptionMenu(
                'Bits de parada', serialTemp.getStopBits())
            self.text = tk.Entry(self.frame)
            self.text.grid(row=5, column=0, padx=5)
            self.buttonFile = tk.Button(
                self.frame, text='Salvar como', command=self.setPath)
            self.buttonFile.grid(row=5, column=1, padx=5)

    def fixFilePath(self, filePath, selectedType):
        extension = None
        format = selectedType.get()
        for i in self.fileTypes:
            if format in i:
                extension = i[1]
                break
        fixedFilePath = filePath
        if extension and not (fixedFilePath.endswith(extension)):
            fixedFilePath = fixedFilePath + extension
        return fixedFilePath
    
    def shouldOverwrite(self):
        self.bell()
        answer = tk.messagebox.askquestion(self, message='Sobrescrever arquivo?')
        if answer == 'yes':
            return True
        return False

    def setPath(self):
        selectedType = tk.StringVar()
        filePath = tk.filedialog.asksaveasfilename(
            filetypes=self.fileTypes,
            typevariable=selectedType)
        fixedFilePath = self.fixFilePath(filePath, selectedType)
        if len(fixedFilePath) != len(filePath):
            if (not os.path.isfile(fixedFilePath)) or self.shouldOverwrite():
                self.text.delete(0, tk.END)
                self.text.insert(0, fixedFilePath)
        else:
            self.text.delete(0, tk.END)
            self.text.insert(0, fixedFilePath)

    def validate(self):
        self.comsettings['port'] = self.port.get()
        self.comsettings['baudrate'] = self.baudrate.get()
        self.comsettings['bytesize'] = self.bytesize.get()
        self.comsettings['parity'] = self.parity.get()
        self.comsettings['stopbits'] = self.stopbits.get()

        # Corrige valores para que a serial possa entender
        parity = 'N'
        if self.comsettings['parity'] == 'Ímpar':
            parity = 'O'
        elif self.comsettings['parity'] == 'Par':
            parity = 'E'
        self.comsettings['parity'] = parity

        stopbits = serial.STOPBITS_ONE
        if self.comsettings['stopbits'] == '1.5':
            stopbits = serial.STOPBITS_ONE_POINT_FIVE
        elif self.comsettings['stopbits'] == '2':
            stopbits = serial.STOPBITS_TWO
        self.comsettings['stopbits'] = stopbits

        bytesize = serial.EIGHTBITS
        if self.comsettings['bytesize'] == '5':
            bytesize = serial.FIVEBITS
        elif self.comsettings['bytesize'] == '6':
            bytesize = serial.SIXBITS
        elif self.comsettings['bytesize'] == '7':
            bytesize = serial.SEVENBITS
        self.comsettings['bytesize'] = bytesize

        filePath = self.text.get()
        resultado = False
        try:
            validate_filepath(filePath, platform='auto')
            resultado = True
        except ValidationError:
            tk.messagebox.showerror('Erro de arquivo', 'Caminho inválido')
            resultado = False
        return resultado

    def apply(self):
        if self.callback:
            self.callback(self.comsettings, self.text.get())


