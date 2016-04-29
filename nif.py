import sys
from PyQt4 import QtCore,QtGui,uic
from controller.controller import *

form_class = uic.loadUiType("nif.ui")[0]

class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        borrar_anterior()
        QtGui.QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.generarButton.clicked.connect(self.generarButton_clicked)

    def generarButton_clicked(self):
        provincia = self.provincia.text()
        ciudad  = self.ciudad.text()
        numeroInicial = int(self.numeroInicial.text())
        cantidad = int(self.cantidad.text())

        #if ciudad < 10:
        #	ciudad = '0'+str(ciudad)

        generar_codigos(provincia,ciudad,numeroInicial,cantidad)

app = QtGui.QApplication(sys.argv)
MyWindow = MyWindowClass(None)
MyWindow.show()
app.exec_()
