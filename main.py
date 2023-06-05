from PyQt5 import QtCore, QtGui, QtWidgets
from PIL.ImageQt import ImageQt
from PIL import Image
import find_max_clique as mc

import json
import os
import time

import smtplib
import email.mime.multipart
import email.mime.application
import email.mime.text
from email.utils import formataddr
from email.header import Header




class Ui_MainWin(object):
    def setupUi(self, MainWin):
        MainWin.setObjectName("MainWin")
        MainWin.resize(1060, 750)
        self.centralwidget = QtWidgets.QWidget(MainWin)
        self.centralwidget.setStyleSheet("background-color: rgb(234, 240, 255);")
        self.centralwidget.setObjectName("centralwidget")
        font = QtGui.QFont()
        font.setPointSize(10)

        self.label_file = QtWidgets.QLabel(self.centralwidget)
        self.label_file.setGeometry(QtCore.QRect(50, 100, 640, 480))
        self.label_file.setFont(font)
        self.label_file.setObjectName("label_file")


        font = QtGui.QFont()
        font.setPointSize(10)

        self.graph = QtWidgets.QLabel(self.centralwidget)
        self.graph.setGeometry(QtCore.QRect(100, 100, 300, 300))
        self.graph.setObjectName("graph")

        self.file = QtWidgets.QPushButton(self.centralwidget)
        self.file.setGeometry(QtCore.QRect(50, 50, 300, 37))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.file.setFont(font)
        self.file.setStyleSheet("background-color: rgb(37, 74, 111);\n"
"color: rgb(255, 255, 255);\n"
"border: 0;")
        self.file.setObjectName("file")

        MainWin.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWin)
        QtCore.QMetaObject.connectSlotsByName(MainWin)

    def retranslateUi(self, MainWin):
        _translate = QtCore.QCoreApplication.translate
        MainWin.setWindowTitle(_translate("MainWin", "Поиск максимальной клики"))
        self.file.setText(_translate("MainWin", "Загрузить граф"))
        self.file.clicked.connect(lambda: self.add_file())
        self.label_file.setText(_translate("MainWin", "Не загружено"))

    def preparation(self):
        pass

    def add_file(self):
        path = QtWidgets.QFileDialog.getOpenFileName()[0]
        self.label_file.setText(str(path))
        clique_answer = mc.max_clique_finder.find(path)
        image = clique_answer['image']
        clique = clique_answer['clique']
        im = ImageQt(image).copy()
        self.graph.setPixmap(QtGui.QPixmap.fromImage(im))
        self.graph.resize(640, 480)
        #self.graph.move(50, 50)

        print(clique_answer)
        print(path)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWin = QtWidgets.QMainWindow()
    ui = Ui_MainWin()
    ui.setupUi(MainWin)
    MainWin.show()

    ui.preparation()

    sys.exit(app.exec_())
