'''
Contains the complete GUI-handling.
'''
import const
from ui import Ui_MainWindow as ui
from cam_thread import Threading
from config import Config

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import subprocess
import os
import time

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
        QObject.__init__(self, parent)

        self.config = Config()
        self.ui = ui()
        self.ui.setupUi(parent)

        self.initializeButton(self.ui.btSd)
        self.initializeButton(self.ui.btUsb)
        self.initializeButton(self.ui.btConfig)
        self.initializeButton(self.ui.btAbbruch)
        self.initializeButton(self.ui.btUntenRechts)

        # only show config-button if no configuration
        # TODO: or if the -config-parameter was used
        if self.config.config_available:
            self.ui.btConfig.hide()
        else:
            self.ui.btConfig.hide()

        self.preview = QPixmap()
        self.sdState = const.MEMSTATE_INIT
        self.usbState = const.MEMSTATE_INIT

        '''
        Timer initialisieren
        '''
        # fuer slot_bist
        self.timer_bist = QTimer(parent)
        self.timer_bist.setInterval(self.config.bist_interval)

        # nur fuer state countdown
        self.count_timer = QTimer(parent)
        self.count_timer.setInterval(1000)
        self.counter = 0
        '''
        nur als Abbbruch bei Bildern
        '''
        self.setButtonImg(self.ui.btConfig, const.IMG_GEAR)
        self.setButtonImg(self.ui.btAbbruch, const.IMG_ABORT)
        self.ui.btAbbruch.hide()

        '''
        Signal/Slot-Verbindungen
        '''
        self.ui.btUntenRechts.clicked.connect(self.slot_btUntenRechts)
        self.ui.btAbbruch.clicked.connect(self.slot_btAbbruch)
        self.ui.btSd.clicked.connect(self.slot_btSd)
        self.ui.btUsb.clicked.connect(self.slot_btUsb)
        self.ui.btConfig.clicked.connect(self.slot_btConfig)

        self.count_timer.timeout.connect(self.slot_countdown)
        self.timer_bist.timeout.connect(self.slot_bist)

        parent.sigResize.connect(self.updateGui)
        parent.showFullScreen()

        self.thread = Threading(parent)
        self.thread.sig_live_view.connect(self.slot_preview)
        self.thread.sig_photo.connect(self.slot_image)

        ''' start '''
        self.changeState(const.STATE_LIVE)

        self.usbDestPath = self.config.usb_path
        self.usbOutputPath = ""
        self.checkMemory()


    def updateGui(self):
        self.ui.gui.setGeometry(self.ui.centralwidget.geometry())
        self.ui.bild.setGeometry(self.ui.centralwidget.geometry())

        self.ui.bild.raise_()
        self.ui.gui.raise_()

    def initializeButton(self, button):
        '''
        Resizing
        '''
        size = button.size()
        size.setWidth(size.width() * self.config.knob_resize_factor)
        size.setHeight(size.height() * self.config.knob_resize_factor)
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
            button.setIconSize(QSize(int(button.width() * self.config.knob_icon_factor),
                                     int(button.height() * self.config.knob_icon_factor)))
            button.show()

    def checkSdState(self):
        '''
        - SD vorhanden
        - SD genug Platz
        '''
        sd_space = self.thread.get_available_space()
        if sd_space < 0:
            result = const.MEMSTATE_MISSING
            return const.MEMSTATE_MISSING
        elif sd_space < self.config.critical_space:
            return const.MEMSTATE_FULL
        else:
            return const.MEMSTATE_OK

    def checkUsbState(self):
        '''
        - USB vorhanden
        - USB genug Platz
        '''
        try:
            p = subprocess.Popen(['df','-l','--output=target,iavail'], stdout=subprocess.PIPE)
            out, err = p.communicate()
        except:
            out = b"/media/pi/ 500000000"

        self.usb_dir = False
        for line in out.splitlines():
            if b"/media/pi/" in line:
                self.usb_dir, availableSpace = line.split()
                self.usb_dir = self.usb_dir.decode()

        if not self.usb_dir:
            return const.MEMSTATE_MISSING
        elif int(availableSpace) < self.config.critical_space:
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
            
            # create the directory if new USB-memory detected
            if usbState != const.MEMSTATE_MISSING:
                if (self.usbState == const.MEMSTATE_MISSING
                        or self.usbState == const.MEMSTATE_INIT):
                    # create a new directory
                    self.usbOutputPath = self.usb_dir + self.usbDestPath
                    try:
                        os.makedirs(self.usbOutputPath)
                    except:
                        print("Path %s could not be created.", self.usbOutputPath)
            
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
            self.setButtonImg(self.ui.btUntenRechts, const.IMG_CAM)
            self.ui.btConfig.show()
            self.thread.start_live()
            self.timer_bist.start()

        elif state == const.STATE_COUNT:
            '''
            - kein Knopf sichtbar (ausser Fehler/Warnungen)
            - Zeige Label
            - Starte Countdown
            '''
            self.counter = self.config.countdown
            self.ui.lblZahl.setText(str(self.counter))
            self.ui.lblZahl.show()
            self.count_timer.start(1000)
            self.timer_bist.stop()

        elif state == const.STATE_BILD:
            self.count_timer.stop()
            self.thread.capture_image()
        self.state = state
        
    def showImage(self, image):
        '''
        Zeigt das Bild auf dem GUI. Genutzt für Foto + Liveview
        :param image:
        '''
        self.preview.loadFromData(image)
        self.ui.bild.setPixmap(self.preview.scaled(
            self.ui.bild.width(),
            self.ui.bild.height(),
            self.config.image_resize_type))
        self.ui.bild.setAlignment(Qt.AlignHCenter)
        self.ui.bild.setAlignment(Qt.AlignCenter)
        self.ui.bild.show()

    def slot_countdown(self):
        '''
        Slot fuer Timer-Signal, zaehlt runter und startet Foto bei 0
        '''
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
            self.changeState(const.STATE_COUNT)
        elif self.state == const.STATE_BILD:
            if not self.usb_dir:
                print("USB nicht verfuegbar")
            else:
                filename = self.usbOutputPath + "/" + time.strftime(self.config.usb_file_string)
                self.thread.store_last(filename)
                
            self.changeState(const.STATE_LIVE)
            self.checkMemory()
        else:
            print("Invalid state")
            self.changeState(const.STATE_LIVE)

    def slot_btAbbruch(self):
        '''
        Knopf:
        - Bild verwerfen (Bild loeschen)
        - zurueck zu Liveview
        '''
        self.thread.dismiss_last()
        self.changeState(const.STATE_LIVE)

    def slot_btSd(self):
        '''
        Knopf:
        - Warnung/Fehler ignorieren: SD-Karte
        '''
        self.ui.btSd.hide()

    def slot_btUsb(self):
        '''
        Knopf:
        - Warnung/Fehler ignorieren: USB-Stick
        '''
        self.ui.btUsb.hide()

    def slot_btConfig(self):
        '''
        Knopf:
        - Konfiguration/Debug
        '''
        self.changeState(const.STATE_BILD)

    def slot_preview(self, image):
        '''
        Receiver-slot fuer Liveview (nur im RAM)
        '''
        self.showImage(image)
        
    def slot_image(self, image):
        '''
        Receiver-slot fuer Fotos
        '''
        self.setButtonImg(self.ui.btUntenRechts, const.IMG_OK)
        self.ui.btAbbruch.show()

        self.showImage(image)
        
    def slot_bist(self):
        self.checkMemory()
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = MainWindowB()
    test = Box(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())