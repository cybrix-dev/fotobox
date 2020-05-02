# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config_gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(979, 458)
        font = QtGui.QFont()
        font.setPointSize(25)
        Dialog.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")
        self.user = QtWidgets.QWidget()
        self.user.setObjectName("user")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.user)
        self.gridLayout_2.setVerticalSpacing(30)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.labTransparency = QtWidgets.QLabel(self.user)
        self.labTransparency.setObjectName("labTransparency")
        self.gridLayout_2.addWidget(self.labTransparency, 1, 2, 1, 1)
        self.slideCountdown = QtWidgets.QSlider(self.user)
        self.slideCountdown.setMaximum(30)
        self.slideCountdown.setProperty("value", 3)
        self.slideCountdown.setOrientation(QtCore.Qt.Horizontal)
        self.slideCountdown.setObjectName("slideCountdown")
        self.gridLayout_2.addWidget(self.slideCountdown, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.user)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.labCountdown = QtWidgets.QLabel(self.user)
        self.labCountdown.setObjectName("labCountdown")
        self.gridLayout_2.addWidget(self.labCountdown, 0, 2, 1, 1)
        self.slideTransparency = QtWidgets.QSlider(self.user)
        self.slideTransparency.setMaximum(100)
        self.slideTransparency.setSingleStep(5)
        self.slideTransparency.setPageStep(20)
        self.slideTransparency.setProperty("value", 15)
        self.slideTransparency.setOrientation(QtCore.Qt.Horizontal)
        self.slideTransparency.setObjectName("slideTransparency")
        self.gridLayout_2.addWidget(self.slideTransparency, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.user)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.ckImageFit = QtWidgets.QCheckBox(self.user)
        self.ckImageFit.setIconSize(QtCore.QSize(25, 25))
        self.ckImageFit.setObjectName("ckImageFit")
        self.gridLayout_2.addWidget(self.ckImageFit, 2, 0, 1, 3)
        self.tabWidget.addTab(self.user, "")
        self.system = QtWidgets.QWidget()
        self.system.setObjectName("system")
        self.tabWidget.addTab(self.system, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Konfiguration"))
        self.labTransparency.setText(_translate("Dialog", "15%"))
        self.label_2.setText(_translate("Dialog", "Transparenz Kamerasymbol"))
        self.labCountdown.setText(_translate("Dialog", "3s"))
        self.label.setText(_translate("Dialog", "Länge Countdown"))
        self.ckImageFit.setText(_translate("Dialog", "Bildgröße an Monitor anpassen"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.user), _translate("Dialog", "Anwender"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.system), _translate("Dialog", "System"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
