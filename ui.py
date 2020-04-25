# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(853, 683)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gui = QtWidgets.QFrame(self.centralwidget)
        self.gui.setGeometry(QtCore.QRect(10, 10, 493, 683))
        self.gui.setObjectName("gui")
        self.gridLayout = QtWidgets.QGridLayout(self.gui)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.btUntenRechts = QtWidgets.QPushButton(self.gui)
        self.btUntenRechts.setMinimumSize(QtCore.QSize(100, 100))
        self.btUntenRechts.setFlat(True)
        self.btUntenRechts.setObjectName("btUntenRechts")
        self.gridLayout.addWidget(self.btUntenRechts, 3, 2, 1, 1)
        self.btUsb = QtWidgets.QPushButton(self.gui)
        self.btUsb.setMinimumSize(QtCore.QSize(175, 100))
        self.btUsb.setFlat(True)
        self.btUsb.setObjectName("btUsb")
        self.gridLayout.addWidget(self.btUsb, 0, 0, 1, 1)
        self.btSd = QtWidgets.QPushButton(self.gui)
        self.btSd.setMinimumSize(QtCore.QSize(175, 100))
        self.btSd.setFlat(True)
        self.btSd.setObjectName("btSd")
        self.gridLayout.addWidget(self.btSd, 1, 0, 1, 1)
        self.btConfig = QtWidgets.QPushButton(self.gui)
        self.btConfig.setMinimumSize(QtCore.QSize(100, 100))
        self.btConfig.setFlat(True)
        self.btConfig.setObjectName("btConfig")
        self.gridLayout.addWidget(self.btConfig, 0, 2, 1, 1)
        self.lblZahl = QtWidgets.QLabel(self.gui)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.lblZahl.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(300)
        self.lblZahl.setFont(font)
        self.lblZahl.setScaledContents(True)
        self.lblZahl.setAlignment(QtCore.Qt.AlignCenter)
        self.lblZahl.setObjectName("lblZahl")
        self.gridLayout.addWidget(self.lblZahl, 1, 1, 2, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 1, 1, 1)
        self.btAbbruch = QtWidgets.QPushButton(self.gui)
        self.btAbbruch.setMinimumSize(QtCore.QSize(100, 100))
        self.btAbbruch.setFlat(True)
        self.btAbbruch.setObjectName("btAbbruch")
        self.gridLayout.addWidget(self.btAbbruch, 3, 0, 1, 1)
        self.bild = QtWidgets.QLabel(self.centralwidget)
        self.bild.setGeometry(QtCore.QRect(360, 360, 231, 331))
        self.bild.setObjectName("bild")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btUntenRechts.setText(_translate("MainWindow", "Start + OK"))
        self.btUsb.setText(_translate("MainWindow", "USB"))
        self.btSd.setText(_translate("MainWindow", "SD"))
        self.btConfig.setText(_translate("MainWindow", "Config"))
        self.lblZahl.setText(_translate("MainWindow", "3"))
        self.btAbbruch.setText(_translate("MainWindow", "Abbruch"))
        self.bild.setText(_translate("MainWindow", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
