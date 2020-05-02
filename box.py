'''
Contains the complete GUI-handling.
'''
import const
from main_gui import Ui_MainWindow as ui
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
        super().__init__(parent)

        # TODO: extract parameter for system-config from CLI-parameters
        self.config = Config(parent, const.INI_FILE, False)
        self.ui = ui()
        self.ui.setupUi(parent)

        self.initialize_button(self.ui.btSd)
        self.initialize_button(self.ui.btUsb)
        self.initialize_button(self.ui.btConfig)
        self.initialize_button(self.ui.btAbbruch)
        self.initialize_button(self.ui.btAccept)

        # only show config-button if no configuration
        # TODO: or if the -config-parameter was used
        self.show_config = True

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
        self.set_button_imgage(self.ui.btConfig, const.IMG_GEAR)
        self.set_button_imgage(self.ui.btAbbruch, const.IMG_ABORT)
        self.set_button_imgage(self.ui.btAccept, const.IMG_OK)
        self.set_button_imgage(self.ui.btTrigger, const.IMG_CAM)
        self.ui.btAbbruch.hide()

        '''
        Signal/Slot-Verbindungen
        '''
        self.ui.btAccept.clicked.connect(self.slot_btAccept)
        self.ui.btTrigger.clicked.connect(self.slot_btTrigger)
        self.ui.btAbbruch.clicked.connect(self.slot_btAbbruch)
        self.ui.btSd.clicked.connect(self.slot_btSd)
        self.ui.btUsb.clicked.connect(self.slot_btUsb)
        self.ui.btConfig.clicked.connect(self.slot_btConfig)

        self.count_timer.timeout.connect(self.slot_countdown)
        self.timer_bist.timeout.connect(self.slot_bist)

        self.config.sig_finished.connect(self.slot_update_config)

        parent.sigResize.connect(self.update_gui)
        parent.showFullScreen()

        # setup camera + camera-thread
        self.thread = Threading(parent, self.config.camera_memory)

        self.thread.sig_live_view.connect(self.slot_preview)
        self.thread.sig_photo.connect(self.slot_image)

        self.usbDestPath = self.config.usb_path
        self.usbOutputPath = ""
        self.check_memory()

        # start, will also start threading
        self.changeState(const.STATE_LIVE)

    def update_gui(self):
        self.ui.gui.setGeometry(self.ui.centralwidget.geometry())
        self.ui.bild.setGeometry(self.ui.centralwidget.geometry())
        self.ui.lblZahl.setGeometry(self.ui.centralwidget.geometry())

        self.ui.bild.raise_()
        self.ui.lblZahl.raise_()
        self.ui.gui.raise_()

    def initialize_button(self, button):
        '''
        Resizing
        '''
        size = button.size()
        size.setWidth(size.width() * self.config.knob_resize_factor)
        size.setHeight(size.height() * self.config.knob_resize_factor)
        button.setFixedSize(size)

    def set_button_imgage(self, button, filename, opacity=1):
        '''
        - wenn kein Dateiname, dann Knopf verstecken
        - Setze Bild fuer Knopf/Anpassen der Groesse
        - anzeigen
        '''
        if not filename:
            button.hide()
        else:
            button.show()
            button.setText("")

            if opacity < 1:
                orgPix = QPixmap(filename)
                transparent = QPixmap(orgPix.size())
                transparent.fill(Qt.transparent)
                painter = QPainter(transparent)
                painter.setOpacity(opacity)
                painter.drawPixmap(0, 0, orgPix)
                painter.end()
                icon = QIcon(transparent)
            else:
                icon = QIcon(filename)
            button.setIcon(icon)
            # 10% vom Rand platz
            button.setIconSize(QSize(int(button.width() * self.config.knob_icon_factor),
                                     int(button.height() * self.config.knob_icon_factor)))
            button.show()

    def show_config_button(self, show):
        if show and self.show_config:
            self.ui.btConfig.show()
        else:
            self.ui.btConfig.hide()

    def check_sd_state(self):
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

    def check_usb_state(self):
        '''
        - USB vorhanden
        - USB genug Platz
        '''
        try:
            p = subprocess.Popen(['df','-l','--output=target,iavail'], stdout=subprocess.PIPE)
            out, err = p.communicate()
        except:
            out = self.config.usb_root + b"/usb-stick 50000"

        self.usb_dir = False
        for line in out.splitlines():
            if self.config.usb_root in line:
                self.usb_dir, availableSpace = line.split()
                self.usb_dir = self.usb_dir.decode() + "/"

        if not self.usb_dir:
            return const.MEMSTATE_MISSING
        elif int(availableSpace) < self.config.critical_space:
            return const.MEMSTATE_FULL
        else:
            return const.MEMSTATE_OK

    def check_memory(self):
        '''
        Check:
        - SD-Karte vorhanden?
        - genug Platz auf Karte?
        - USB-Stick vorhanden?
        - genug Platz auf Stick?
        '''
        usbState = self.check_usb_state()
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
                        print("Path could not be created: ", self.usbOutputPath)
            
            if usbState == const.MEMSTATE_OK:
                img = False
            elif usbState == const.MEMSTATE_FULL:
                img = const.IMG_USB_FULL
            elif usbState == const.MEMSTATE_MISSING:
                img = const.IMG_USB_MISSING
            else:
                img = const.IMG_USB
            self.set_button_imgage(self.ui.btUsb, img)
            self.usbState = usbState

        sdState = self.check_sd_state()
        if sdState != self.sdState:
            if sdState == const.MEMSTATE_OK:
                img = False
            elif sdState == const.MEMSTATE_FULL:
                img = const.IMG_SD_FULL
            elif sdState == const.MEMSTATE_MISSING:
                img = const.IMG_SD_MISSING
            else:
                img = const.IMG_SD
            self.set_button_imgage(self.ui.btSd, img)
            self.sdState = sdState

    def changeState(self, state):
        '''
        - alles verstecken
        - nur anzeigen, was gebraucht wird
        - Status von SD/USB bleibt
        '''
        self.ui.lblZahl.hide()

        self.show_trigger(False)
        self.ui.btAbbruch.hide()
        self.ui.btAccept.hide()
        self.show_config_button(False)

        if state == const.STATE_LIVE:
            '''
            - Zeige Kameraknopf
            - kein Countdown
            - kein Abbruchknopf
            '''
            self.show_trigger(True)
            self.show_config_button(True)
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
        
        if self.config.image_mirrored:
            self.preview = self.preview.transformed(QTransform().scale(-1, 1))
            
        self.ui.bild.setPixmap(self.preview.scaled(self.ui.bild.width(),
                                                   self.ui.bild.height(),
                                                   self.config.image_resize_type))
        self.ui.bild.setAlignment(Qt.AlignHCenter)
        self.ui.bild.setAlignment(Qt.AlignCenter)
        self.ui.bild.show()

    def show_trigger(self, show):
        if show:
            self.set_button_imgage(self.ui.btTrigger, const.IMG_CAM, self.config.trigger_transparency)
        else:
            # hide can not be used, this button is also a spacer
            self.ui.btTrigger.setText("")
            self.ui.btTrigger.setIcon(QIcon())

        self.ui.btTrigger.setDisabled(not show)

    def slot_countdown(self):
        '''
        Slot fuer Timer-Signal, zaehlt runter und startet Foto bei 0
        '''
        self.counter -= 1
        if self.counter > 0:
            self.ui.lblZahl.setText(str(self.counter))
        else:
            self.changeState(const.STATE_BILD)

    def slot_btTrigger(self):
        '''
        Knopf:
        - Countdown starten (Bild mit Kamera)
        '''
        if self.state == const.STATE_LIVE:
            self.changeState(const.STATE_COUNT)

    def slot_btAccept(self):
        '''
        Knopf:
        - Bild akzeptieren (Bild Checkbox)
        - zurueck zu LiveView
        '''
        if not self.usb_dir:
            print("USB nicht verfuegbar")
        else:
            filename = self.usbOutputPath + "/" + time.strftime(self.config.usb_file_string)
            self.thread.store_last(filename)

        self.changeState(const.STATE_LIVE)
        self.check_memory()

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
        self.config.open_config()

    def slot_preview(self, image):
        '''
        Receiver-slot fuer Liveview (nur im RAM)
        '''
        self.showImage(image)
        
    def slot_image(self, image):
        '''
        Receiver-slot fuer Fotos
        '''
        self.show_trigger(False)
        self.ui.btAccept.show()
        self.ui.btAbbruch.show()

        self.showImage(image)
        
    def slot_bist(self):
        self.check_memory()

    def slot_update_config(self):
        # GUI
        self.changeState(self.state)
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = MainWindowB()
    test = Box(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())