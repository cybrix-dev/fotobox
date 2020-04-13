'''
Created on 24.02.2020

@author: t.starke
'''
from ui import Ui_MainWindow as ui
import const
from cam import Camera

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import subprocess


class MainWindowB(QMainWindow):

    sigResize = pyqtSignal()

    def resizeEvent(self, *args, **kwargs):
        self.sigResize.emit()
        return QMainWindow.resizeEvent(self, *args, **kwargs)


class Box(QObject):
    '''
    classdocs
    '''

    def __init__(self, parent):

        '''
        Constructor
        '''
        super(Box, self).__init__()
        self.ui = ui()
        self.ui.setupUi(parent)

        self.initializeButton(self.ui.btSd)
        self.initializeButton(self.ui.btUsb)
        self.initializeButton(self.ui.btConfig)
        self.initializeButton(self.ui.btAbbruch)
        self.initializeButton(self.ui.btUntenRechts)

        self.sdState = const.MEMSTATE_INIT
        self.usbState = const.MEMSTATE_INIT

        '''
        Timer initialisieren
        '''
        # wird in status live getriggert
        self.bist_timer = QTimer(parent)
        self.bist_timer.setInterval(const.BIST_INTERVAL)

        # nur fuer state countdown
        self.count_timer = QTimer(parent)
        self.count_timer.setInterval(const.COUNTDOWN_START * 1000)

        '''
        nur als Abbbruch bei Bildern
        '''
        self.setButtonImg(self.ui.btConfig, const.IMG_GEAR)
        self.setButtonImg(self.ui.btAbbruch, const.IMG_ABORT)
        self.ui.btAbbruch.hide()

        print("test environment")
        self.checkMemory()

        '''
        Signal/Slot-Verbindungen
        '''
        self.ui.btUntenRechts.clicked.connect(self.slot_btUntenRechts)
        self.ui.btAbbruch.clicked.connect(self.slot_btAbbruch)
        self.ui.btSd.clicked.connect(self.slot_btSd)
        self.ui.btUsb.clicked.connect(self.slot_btUsb)
        self.ui.btConfig.clicked.connect(self.slot_btConfig)


        self.count_timer.timeout.connect(self.slot_countdown)
        self.bist_timer.timeout.connect(self.slot_bist)

        parent.sigResize.connect(self.updateGui)
        parent.showFullScreen()

        self.cam = Camera()

        ''' start '''
        self.changeState(const.STATE_LIVE)

    def updateGui(self):
        self.ui.gui.setGeometry(self.ui.centralwidget.geometry())
        self.ui.bild.setGeometry(self.ui.centralwidget.geometry())
        self.ui.video.setGeometry(self.ui.centralwidget.geometry())

        self.ui.bild.raise_()
        self.ui.video.raise_()
        self.ui.gui.raise_()

        print("Resize")


    def initializeButton(self, button):
        '''
        Resizing
        '''
        size = button.size()
        size.setWidth(size.width() * const.KNOB_RESIZE_FACTOR)
        size.setHeight(size.height() * const.KNOB_RESIZE_FACTOR)
        button.setFixedSize(size)

    def setButtonImg(self, button, filename):
        '''
        - wenn kein Dateiname, dann Knopf verstecken
        - Setze Bild fuer Knopf/Anpassen der Groesse
        - anzeigen
        '''
        if not filename:
            button.hide()
        else:
            button.setText("")
            button.setIcon(QIcon(filename))
            # 10% vom Rand platz
            button.setIconSize(QSize(button.width() * const.KNOB_ICON_FACTOR,
                                     button.height() * const.KNOB_ICON_FACTOR))
            button.show()

    def checkSdState(self):
        '''
        - SD vorhanden
        - SD genug Platz
        '''
        print("Todo: check SD-Card")
        return const.MEMSTATE_OK

    def checkUsbState(self):
        '''
        - USB vorhanden
        - USB genug Platz
        '''
        p = subprocess.Popen(['df','-l','--output=target,iavail'], stdout=subprocess.PIPE)
        out, err = p.communicate()

        self.usb_dir = False
        for line in out.splitlines():
            if b'/media/pi/' in line:
                self.usb_dir, availableSpace = line.split()
                print(self.usb_dir)
                print(availableSpace)

        if not self.usb_dir:
            return const.MEMSTATE_MISSING
        elif int(availableSpace) < 50000:
            return const.MEMSTATE_FULL
        else:
            return const.MEMSTATE_OK

    def checkMemory(self):
        '''
        Check:
        - SD-Karte vorhanden?
        - genug Platz auf Karte?
        - USB-Stick vorhanden?
        - genug Platz auf Stick?
        '''
        usbState = self.checkUsbState()
        if usbState != self.usbState:
            if usbState == const.MEMSTATE_OK:
                img = False
            elif usbState == const.MEMSTATE_FULL:
                img = const.IMG_USB_FULL
            elif usbState == const.MEMSTATE_MISSING:
                img = const.IMG_USB_MISSING
            else:
                img = const.IMG_USB
            self.setButtonImg(self.ui.btUsb, img)
            self.usbState = usbState

        sdState = self.checkSdState()
        if sdState != self.sdState:
            if sdState == const.MEMSTATE_OK:
                img = False
            elif sdState == const.MEMSTATE_FULL:
                img = const.IMG_SD_FULL
            elif sdState == const.MEMSTATE_MISSING:
                img = const.IMG_SD_MISSING
            else:
                img = const.IMG_SD
            self.setButtonImg(self.ui.btSd, img)
            self.sdState = sdState

    def changeState(self, state):
        '''
        - alles verstecken
        - nur anzeigen, was gebraucht wird
        - Status von SD/USB bleibt
        '''
        self.ui.bild.hide()
        self.ui.video.hide()

        self.ui.lblZahl.hide()

        self.ui.btAbbruch.hide()
        self.ui.btConfig.hide()
        self.ui.btUntenRechts.hide()

        if state == const.STATE_LIVE:
            '''
            - Zeige Kameraknopf
            - kein Countdown
            - kein Abbruchknopf
            '''
            print("Stream video")
            self.ui.video.show()
            self.setButtonImg(self.ui.btUntenRechts, const.IMG_CAM)
            self.ui.btConfig.show()

        elif state == const.STATE_COUNT:
            '''
            - kein Knopf sichtbar (ausser Fehler/Warnungen)
            - Zeige Label
            - Starte Countdown
            '''
            self.counter = const.COUNTDOWN_START
            self.ui.lblZahl.setText(str(self.counter))
            self.ui.lblZahl.show()
            self.count_timer.start(1000)

        elif state == const.STATE_BILD:
            self.count_timer.stop()

            print("Bild runterladen + anzeigen")
            picture = QPixmap("./icons/test.jpg").scaled(self.ui.bild.width(), self.ui.bild.height(), Qt.KeepAspectRatioByExpanding)

            self.ui.bild.setPixmap(picture)
            self.ui.bild.setAlignment(Qt.AlignHCenter)
            self.ui.bild.setAlignment(Qt.AlignCenter)
            self.ui.bild.show()

            self.setButtonImg(self.ui.btUntenRechts, const.IMG_OK)
            self.ui.btAbbruch.show()

        self.state = state

    def slot_bist(self):
        self.checkMemory()
        self.bist_timer.start(const.BIST_INTERVAL)

    def slot_countdown(self):
        self.counter -= 1
        if self.counter > 0:
            self.ui.lblZahl.setText(str(self.counter))
        else:
            self.changeState(const.STATE_BILD)

    def slot_btUntenRechts(self):
        '''
        Knopf:
        - Countdown starten (Bild mit Kamera)
        - Bild akzeptieren (Bild Checkbox)
        '''
        if self.state == const.STATE_LIVE:
            # self.changeState(const.STATE_COUNT)
            self.changeState(const.STATE_BILD)
        elif self.state == const.STATE_BILD:
            print("Bild speichern")
            self.changeState(const.STATE_LIVE)
        else:
            print("Invalid state")
            self.changeState(const.STATE_LIVE)

    def slot_btAbbruch(self):
        '''
        Knopf:
        - Bild verwerfen (Bild loeschen)
        - zurueck zu Liveview
        '''
        print("Bild loeschen")
        self.changeState(const.STATE_LIVE)

    def slot_btSd(self):
        '''
        Knopf:
        - Warnung/Fehler ignorieren: SD-Karte
        '''
        self.ui.btSd.hide()
        print("SD-Status")

    def slot_btUsb(self):
        '''
        Knopf:
        - Warnung/Fehler ignorieren: USB-Stick
        '''
        self.ui.btUsb.hide()
        print("USB-Status")

    def slot_btConfig(self):
        '''
        Knopf:
        - Konfiguration/Debug
        '''
        print("Config")
        picture = self.cam.fetch_preview().scaled(self.ui.bild.width(),
                                                  self.ui.bild.height(),
                                                  Qt.KeepAspectRatioByExpanding)

        self.ui.bild.setPixmap(picture)
        self.ui.bild.setAlignment(Qt.AlignHCenter)
        self.ui.bild.setAlignment(Qt.AlignCenter)
        self.ui.bild.show()



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = MainWindowB()
    test = Box(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())