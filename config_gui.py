# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'config_gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(843, 682)
        font = QtGui.QFont()
        font.setPointSize(25)
        Dialog.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.btDefaults = QtWidgets.QPushButton(Dialog)
        self.btDefaults.setObjectName("btDefaults")
        self.gridLayout.addWidget(self.btDefaults, 1, 1, 1, 1)
        self.btReset = QtWidgets.QPushButton(Dialog)
        self.btReset.setObjectName("btReset")
        self.gridLayout.addWidget(self.btReset, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 2, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")
        self.user = QtWidgets.QWidget()
        self.user.setObjectName("user")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.user)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.user)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.slideCountdown = QtWidgets.QSlider(self.user)
        self.slideCountdown.setStyleSheet(".QSlider {\n"
"    min-height: 55px;\n"
"    max-height: 55px;\n"
"}\n"
"\n"
".QSlider::groove:horizontal {\n"
"    border: 1px solid #262626;\n"
"    height: 5px;\n"
"    margin: 0 12px;\n"
"}\n"
"\n"
".QSlider::handle:horizontal {\n"
"    border: 5px solid #777777;\n"
"    width: 23px;\n"
"    height: 100px;\n"
"    margin: -24px -12px;\n"
"    background: #444444\n"
"}")
        self.slideCountdown.setMaximum(30)
        self.slideCountdown.setProperty("value", 3)
        self.slideCountdown.setOrientation(QtCore.Qt.Horizontal)
        self.slideCountdown.setObjectName("slideCountdown")
        self.gridLayout_2.addWidget(self.slideCountdown, 0, 2, 1, 1)
        self.labCountdown = QtWidgets.QLabel(self.user)
        self.labCountdown.setObjectName("labCountdown")
        self.gridLayout_2.addWidget(self.labCountdown, 0, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.user)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 2)
        self.slideTransparency = QtWidgets.QSlider(self.user)
        self.slideTransparency.setStyleSheet(".QSlider {\n"
"    min-height: 55px;\n"
"    max-height: 55px;\n"
"}\n"
"\n"
".QSlider::groove:horizontal {\n"
"    border: 1px solid #262626;\n"
"    height: 5px;\n"
"    margin: 0 12px;\n"
"}\n"
"\n"
".QSlider::handle:horizontal {\n"
"    border: 5px solid #777777;\n"
"    width: 23px;\n"
"    height: 100px;\n"
"    margin: -24px -12px;\n"
"    background: #444444\n"
"}")
        self.slideTransparency.setMaximum(100)
        self.slideTransparency.setSingleStep(5)
        self.slideTransparency.setProperty("value", 15)
        self.slideTransparency.setOrientation(QtCore.Qt.Horizontal)
        self.slideTransparency.setObjectName("slideTransparency")
        self.gridLayout_2.addWidget(self.slideTransparency, 1, 2, 1, 1)
        self.labTransparency = QtWidgets.QLabel(self.user)
        self.labTransparency.setObjectName("labTransparency")
        self.gridLayout_2.addWidget(self.labTransparency, 1, 3, 1, 1)
        self.ckImageFit = QtWidgets.QCheckBox(self.user)
        self.ckImageFit.setIconSize(QtCore.QSize(25, 25))
        self.ckImageFit.setObjectName("ckImageFit")
        self.gridLayout_2.addWidget(self.ckImageFit, 2, 0, 1, 3)
        self.label_11 = QtWidgets.QLabel(self.user)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 3, 0, 1, 1)
        self.labUsbSpaceIcon = QtWidgets.QLabel(self.user)
        self.labUsbSpaceIcon.setObjectName("labUsbSpaceIcon")
        self.gridLayout_2.addWidget(self.labUsbSpaceIcon, 3, 1, 1, 1)
        self.labUsbSpace = QtWidgets.QLabel(self.user)
        self.labUsbSpace.setObjectName("labUsbSpace")
        self.gridLayout_2.addWidget(self.labUsbSpace, 3, 2, 1, 1)
        self.labCamSpaceType = QtWidgets.QLabel(self.user)
        self.labCamSpaceType.setObjectName("labCamSpaceType")
        self.gridLayout_2.addWidget(self.labCamSpaceType, 4, 0, 1, 1)
        self.labCamSpaceIcon = QtWidgets.QLabel(self.user)
        self.labCamSpaceIcon.setObjectName("labCamSpaceIcon")
        self.gridLayout_2.addWidget(self.labCamSpaceIcon, 4, 1, 1, 1)
        self.labCamSpace = QtWidgets.QLabel(self.user)
        self.labCamSpace.setObjectName("labCamSpace")
        self.gridLayout_2.addWidget(self.labCamSpace, 4, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(228, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 5, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 6, 0, 1, 1)
        self.tabWidget.addTab(self.user, "")
        self.usb = QtWidgets.QWidget()
        self.usb.setObjectName("usb")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.usb)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_5 = QtWidgets.QLabel(self.usb)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 0, 0, 1, 1)
        self.lineUsbRoot = QtWidgets.QLineEdit(self.usb)
        self.lineUsbRoot.setObjectName("lineUsbRoot")
        self.gridLayout_4.addWidget(self.lineUsbRoot, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.usb)
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 1, 0, 1, 1)
        self.lineUsbPath = QtWidgets.QLineEdit(self.usb)
        self.lineUsbPath.setObjectName("lineUsbPath")
        self.gridLayout_4.addWidget(self.lineUsbPath, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.usb)
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 2, 0, 1, 1)
        self.lineUsbFilename = QtWidgets.QLineEdit(self.usb)
        self.lineUsbFilename.setObjectName("lineUsbFilename")
        self.gridLayout_4.addWidget(self.lineUsbFilename, 2, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 380, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem2, 3, 0, 1, 1)
        self.tabWidget.addTab(self.usb, "")
        self.gui = QtWidgets.QWidget()
        self.gui.setObjectName("gui")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.gui)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_10 = QtWidgets.QLabel(self.gui)
        self.label_10.setObjectName("label_10")
        self.gridLayout_7.addWidget(self.label_10, 1, 0, 1, 1)
        self.spinKnobIcon = QtWidgets.QDoubleSpinBox(self.gui)
        self.spinKnobIcon.setProperty("value", 0.75)
        self.spinKnobIcon.setObjectName("spinKnobIcon")
        self.gridLayout_7.addWidget(self.spinKnobIcon, 1, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem3, 0, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gui)
        self.label_9.setObjectName("label_9")
        self.gridLayout_7.addWidget(self.label_9, 0, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 432, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_7.addItem(spacerItem4, 2, 0, 1, 1)
        self.spinKnobResize = QtWidgets.QDoubleSpinBox(self.gui)
        self.spinKnobResize.setDecimals(1)
        self.spinKnobResize.setSingleStep(0.1)
        self.spinKnobResize.setProperty("value", 1.0)
        self.spinKnobResize.setObjectName("spinKnobResize")
        self.gridLayout_7.addWidget(self.spinKnobResize, 0, 1, 1, 1)
        self.tabWidget.addTab(self.gui, "")
        self.camera = QtWidgets.QWidget()
        self.camera.setObjectName("camera")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.camera)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_7 = QtWidgets.QLabel(self.camera)
        self.label_7.setObjectName("label_7")
        self.gridLayout_5.addWidget(self.label_7, 0, 0, 1, 1)
        self.ckImageMirrored = QtWidgets.QCheckBox(self.camera)
        self.ckImageMirrored.setObjectName("ckImageMirrored")
        self.gridLayout_5.addWidget(self.ckImageMirrored, 1, 0, 1, 2)
        self.comboCameraMemory = QtWidgets.QComboBox(self.camera)
        self.comboCameraMemory.setObjectName("comboCameraMemory")
        self.gridLayout_5.addWidget(self.comboCameraMemory, 0, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem5, 2, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem6, 0, 2, 1, 1)
        self.tabWidget.addTab(self.camera, "")
        self.general = QtWidgets.QWidget()
        self.general.setObjectName("general")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.general)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.spinCriticalMemory = QtWidgets.QSpinBox(self.general)
        self.spinCriticalMemory.setMaximum(1000)
        self.spinCriticalMemory.setProperty("value", 50)
        self.spinCriticalMemory.setObjectName("spinCriticalMemory")
        self.gridLayout_3.addWidget(self.spinCriticalMemory, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.general)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.general)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 1)
        self.spinBistInterval = QtWidgets.QSpinBox(self.general)
        self.spinBistInterval.setMaximum(30000)
        self.spinBistInterval.setProperty("value", 5000)
        self.spinBistInterval.setObjectName("spinBistInterval")
        self.gridLayout_3.addWidget(self.spinBistInterval, 2, 1, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 432, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem7, 3, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.general)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 0, 0, 1, 1)
        self.spinLowMemory = QtWidgets.QSpinBox(self.general)
        self.spinLowMemory.setMaximum(1000)
        self.spinLowMemory.setProperty("value", 5)
        self.spinLowMemory.setObjectName("spinLowMemory")
        self.gridLayout_3.addWidget(self.spinLowMemory, 0, 1, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(236, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem8, 0, 2, 1, 1)
        self.tabWidget.addTab(self.general, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 3)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Konfiguration"))
        self.btDefaults.setText(_translate("Dialog", "Standardwerte"))
        self.btReset.setText(_translate("Dialog", "Neustart"))
        self.label.setText(_translate("Dialog", "Länge Countdown"))
        self.labCountdown.setText(_translate("Dialog", "3s"))
        self.label_2.setText(_translate("Dialog", "Transparenz Kamerasymbol"))
        self.labTransparency.setText(_translate("Dialog", "15%"))
        self.ckImageFit.setText(_translate("Dialog", "Bildgröße an Monitor anpassen"))
        self.label_11.setText(_translate("Dialog", "Platz auf USB-Stick"))
        self.labUsbSpaceIcon.setText(_translate("Dialog", "(usb_icon)"))
        self.labUsbSpace.setText(_translate("Dialog", "USB_mem"))
        self.labCamSpaceType.setText(_translate("Dialog", "Platz auf Kamera (SD)"))
        self.labCamSpaceIcon.setText(_translate("Dialog", "(cam_icon)"))
        self.labCamSpace.setText(_translate("Dialog", "CAM_mem"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.user), _translate("Dialog", "Anwender"))
        self.label_5.setText(_translate("Dialog", "Suchpfad für USB-Stick"))
        self.lineUsbRoot.setText(_translate("Dialog", "/media/pi"))
        self.label_6.setToolTip(_translate("Dialog", "<html><head/><body><p>Platzhalter im String (Auswahl):<br>\n"
"%Y - Jahr als 2019<br>\n"
"%y - Jahr als 19<br>\n"
"%m - Monat als 06<br>\n"
"%d - Tag als 01<br>\n"
"%H - Stunde als 00 .. 23<br>\n"
"%M - Minute als 00 .. 59<br>\n"
"%S - Sekunde als 00 .. 59</p></body></html>"))
        self.label_6.setText(_translate("Dialog", "Neues Verzeichnis"))
        self.lineUsbPath.setToolTip(_translate("Dialog", "<html><head/><body><p>Platzhalter im String (Auswahl):<br>\n"
"%Y - Jahr als 2019<br>\n"
"%y - Jahr als 19<br>\n"
"%m - Monat als 06<br>\n"
"%d - Tag als 01<br>\n"
"%H - Stunde als 00 .. 23<br>\n"
"%M - Minute als 00 .. 59<br>\n"
"%S - Sekunde als 00 .. 59</p></body></html>"))
        self.lineUsbPath.setText(_translate("Dialog", "%Y-%m-%d_fotobox"))
        self.label_8.setToolTip(_translate("Dialog", "<html><head/><body><p>Platzhalter im String (Auswahl):<br>\n"
"%Y - Jahr als 2019<br>\n"
"%y - Jahr als 19<br>\n"
"%m - Monat als 06<br>\n"
"%d - Tag als 01<br>\n"
"%H - Stunde als 00 .. 23<br>\n"
"%M - Minute als 00 .. 59<br>\n"
"%S - Sekunde als 00 .. 59</p></body></html>"))
        self.label_8.setText(_translate("Dialog", "Dateiname"))
        self.lineUsbFilename.setToolTip(_translate("Dialog", "<html><head/><body><p>Platzhalter im String (Auswahl):<br>\n"
"%Y - Jahr als 2019<br>\n"
"%y - Jahr als 19<br>\n"
"%m - Monat als 06<br>\n"
"%d - Tag als 01<br>\n"
"%H - Stunde als 00 .. 23<br>\n"
"%M - Minute als 00 .. 59<br>\n"
"%S - Sekunde als 00 .. 59</p></body></html>"))
        self.lineUsbFilename.setText(_translate("Dialog", "%Y-%m-%d_%H-%M-%S.jpg"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.usb), _translate("Dialog", "USB"))
        self.label_10.setText(_translate("Dialog", "Icongröße kleine Knöpfe"))
        self.label_9.setText(_translate("Dialog", "Touchgröße kleine Knöpfe"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.gui), _translate("Dialog", "GUI"))
        self.label_7.setText(_translate("Dialog", "Speichermedium Kamera"))
        self.ckImageMirrored.setText(_translate("Dialog", "Bild gespiegelt"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.camera), _translate("Dialog", "Kamera"))
        self.label_4.setText(_translate("Dialog", "Intervall Speichercheck (ms)"))
        self.label_3.setText(_translate("Dialog", "Kritischer Speicherplatz (MB)"))
        self.label_12.setText(_translate("Dialog", "Niedriger Speicherplatz (MB)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.general), _translate("Dialog", "Allgemein"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
