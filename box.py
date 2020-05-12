'''
Contains the complete GUI-handling.
'''
import const
import logs
from main_gui import Ui_MainWindow as ui
from cam_thread import Threading
from config import Config

from PyQt5.QtCore import pyqtSignal, Qt, QObject, QSize, QTimer
from PyQt5.QtCore import QCommandLineParser, QCommandLineOption, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap, QPainter, QIcon, QTransform

import subprocess
import os
import time
import sys
import logging


class MainWindowB(QMainWindow):

    sigResize = pyqtSignal()

    def resizeEvent(self, *args, **kwargs):
        log = logs.logger.add_module("MainWindowB")
        log.info("Resize")
        self.sigResize.emit()
        return QMainWindow.resizeEvent(self, *args, **kwargs)


class Box(QObject):
    '''
    classdocs
    '''

    def __init__(self, parent, config_mode, log_level=logging.INFO):
        self.log = logs.logger.add_module("Box")
        self.log.warning("__init__(config_mode=%a, log_level=%a)", config_mode, log_level)
        logs.logger.change_level(log_level)
        '''
        Constructor
        '''
        super().__init__(parent)

        # TODO: extract parameter for system-config from CLI-parameters
        self.config = Config(parent, const.INI_FILE, config_mode)
        
        self.log.info("ui()")
        self.ui = ui()
        self.log.info("ui.setupUi()")
        self.ui.setupUi(parent)

        self.log.info("update_gui_elements()")
        self.update_gui_elements()
        
        self.log.debug("initialize members")
        self.preview = QPixmap()
        self.sdState = const.MEMSTATE_INIT
        self.usbState = const.MEMSTATE_INIT
        self.usb_space = -1
        self.cam_space = -1
        self.cam_memory = []
        self.state = const.STATE_INIT

        '''
        Timer initialisieren
        '''
        self.log.debug("Setup timers")

        # fuer slot_bist
        self.timer_bist = QTimer(parent)
        self.timer_bist.setInterval(self.config.bist_interval)

        # nur fuer state countdown
        self.count_timer = QTimer(parent)
        self.count_timer.setInterval(1000)
        self.counter = 0
        
        '''
        Buttons mit Bildern
        '''
        self.log.debug("Setup knob-icons")
        self.set_button_image(self.ui.btConfig, const.IMG_GEAR)
        self.set_button_image(self.ui.btAbbruch, const.IMG_ABORT)
        self.set_button_image(self.ui.btAccept, const.IMG_OK)
        self.set_button_image(self.ui.btTrigger, const.IMG_CAM)
        self.ui.btAbbruch.hide()

        '''
        Signal/Slot-Verbindungen
        '''
        self.log.debug("Setup SIGNAL/SLOTS")
        self.ui.btAccept.clicked.connect(self.slot_btAccept)
        self.ui.btTrigger.clicked.connect(self.slot_btTrigger)
        self.ui.btAbbruch.clicked.connect(self.slot_btAbbruch)
        self.ui.btSd.clicked.connect(self.slot_btSd)
        self.ui.btUsb.clicked.connect(self.slot_btUsb)
        self.ui.btConfig.clicked.connect(self.slot_btConfig)

        self.count_timer.timeout.connect(self.slot_countdown)
        self.timer_bist.timeout.connect(self.slot_bist)

        self.config.sig_finished.connect(self.slot_update_config)
        self.config.sig_reset.connect(self.slot_config_reset)

        parent.sigResize.connect(self.update_gui)
        
        self.log.debug("Display fullscreen for resizing")
        parent.showFullScreen()

        # setup camera + camera-thread
        self.log.debug("Create Cam-thread")
        self.thread = Threading(parent, self.config.camera_memory)
        
        for mem in self.thread.cam.available_memory:
            self.cam_memory.append(mem[0])

        self.thread.sig_live_view.connect(self.slot_preview)
        self.thread.sig_photo.connect(self.slot_image)
        self.thread.sig_error.connect(self.slot_error_preview)
        
        self.usbOutputPath = ""
        
        self.log.debug("Check memory")
        self.check_memory()

        # start, will also start threading
        self.changeState(const.STATE_LIVE)
        
    def update_gui_elements(self):
        self.log.debug("update_gui_elements()")
        self.initialize_button(self.ui.btSd)
        self.initialize_button(self.ui.btUsb)
        self.initialize_button(self.ui.btConfig)
        self.initialize_button(self.ui.btAbbruch)
        self.initialize_button(self.ui.btAccept)

    def update_gui(self):
        self.log.debug("update_gui()")
        self.ui.gui.setGeometry(self.ui.centralwidget.geometry())
        self.ui.bild.setGeometry(self.ui.centralwidget.geometry())
        self.ui.lblZahl.setGeometry(self.ui.centralwidget.geometry())

        self.ui.bild.raise_()
        self.ui.lblZahl.raise_()
        self.ui.gui.raise_()

    def initialize_button(self, button):
        self.log.debug("initialize button()")
        '''
        Resizing
        '''
        size = button.size()
        size.setWidth(int(size.width() * self.config.knob_resize_factor))
        size.setHeight(int(size.height() * self.config.knob_resize_factor))
        button.setFixedSize(size)

        
    def resize_button_icon(self, button):
        width = button.width()
        height = button.height()
        button.setIconSize(
            QSize(int(width * self.config.knob_icon_factor),
                  int(height * self.config.knob_icon_factor)))


    def set_button_image(self, button, filename, opacity=1):
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
            self.resize_button_icon(button)
            # 10% vom Rand platz
            button.show()

    def show_config_button(self, show):
        if show:
            self.ui.btConfig.show()
        else:
            self.ui.btConfig.hide()

    def check_sd_state(self):
        '''
        - SD vorhanden
        - SD genug Platz
        '''
        self.cam_space = self.thread.get_available_space()
        if self.cam_space < 0:
            result = const.MEMSTATE_MISSING
        elif self.cam_space <= self.config.critical_space:
            result = const.MEMSTATE_FULL
        elif self.cam_space <= self.config.low_space:
            result = const.MEMSTATE_LOW
        else:
            result = const.MEMSTATE_OK
            
        return result

    def check_usb_state(self):
        '''
        - USB vorhanden
        - USB genug Platz
        '''
        try:
            p = subprocess.Popen(['df','-l','--output=target,iavail'], stdout=subprocess.PIPE)
            out, _ = p.communicate()
        except:
            out = self.config.usb_root.encode() + b"/usb-stick 50000"

        self.usb_dir = False
        self.usb_space = -1
        for line in out.splitlines():
            line = line.decode()
            if self.config.usb_root in line:
                self.usb_dir, availableSpace = line.split()
                self.usb_space = int(availableSpace)
                self.usb_dir = self.usb_dir + "/"
                break

        if not self.usb_dir:
            return const.MEMSTATE_MISSING
        elif self.usb_space <= self.config.critical_space:
            return const.MEMSTATE_FULL
        elif self.usb_space <= self.config.low_space:
            return const.MEMSTATE_LOW
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
                    self.usbOutputPath = time.strftime(self.usb_dir + self.config.usb_path)
                    try:
                        os.makedirs(self.usbOutputPath)
                    except:
                        self.log.warning("Path could not be created: " + self.usbOutputPath)
            
            if usbState == const.MEMSTATE_OK:
                img = False
            elif usbState == const.MEMSTATE_LOW:
                img = const.IMG_USB_LOW
            elif usbState == const.MEMSTATE_FULL:
                img = const.IMG_USB_FULL
            elif usbState == const.MEMSTATE_MISSING:
                img = const.IMG_USB_MISSING
            else:
                img = const.IMG_USB
            self.set_button_image(self.ui.btUsb, img)
            self.usbState = usbState

        sdState = self.check_sd_state()
        if sdState != self.sdState:
            if sdState == const.MEMSTATE_OK:
                img = False
            elif sdState == const.MEMSTATE_LOW:
                img = const.IMG_SD_LOW
            elif sdState == const.MEMSTATE_FULL:
                img = const.IMG_SD_FULL
            elif sdState == const.MEMSTATE_MISSING:
                img = const.IMG_SD_MISSING
            else:
                img = const.IMG_SD
            self.set_button_image(self.ui.btSd, img)
            self.sdState = sdState

    def changeState(self, state):
        '''
        - alles verstecken
        - nur anzeigen, was gebraucht wird
        - Status von SD/USB bleibt
        '''
        self.log.debug("Change state: %a -> %a", self.state, state)
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
            if self.counter > 0:
                self.ui.lblZahl.setText(str(self.counter))
                self.ui.lblZahl.show()
                self.count_timer.start(1000)
                self.timer_bist.stop()
            else:
                state = const.STATE_BILD
                self.thread.capture_image()

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
            self.set_button_image(self.ui.btTrigger, const.IMG_CAM, self.config.trigger_opacity)
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
            self.log.error("USB nicht verfuegbar")
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
        self.config.open_config(self.usb_space, self.cam_space, self.cam_memory)

    def slot_preview(self, image):
        '''
        Receiver-slot fuer Liveview (nur im RAM)
        '''
        self.showImage(image)
        self.resize_button_icon(self.ui.btTrigger)
        
    def slot_error_preview(self, image):
        '''
        Receiver-slot fuer Preview obwohl Foto angefragt (nur im RAM)
        '''
        self.showImage(image)
        self.ui.btAbbruch.show()
        self.show_trigger(False)
        
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
        
    def slot_config_reset(self):
        QApplication.exit(1) 

class CliParser:
    def __init__(self,app):
        self.log = logs.logger.add_module("CliParser")
        QApplication.setApplicationName("fotobox");
        QApplication.setApplicationVersion("1.0");

        self.parser = QCommandLineParser()
        self.parser.setApplicationDescription("Fotobox")
        self.parser.addHelpOption()
        self.parser.addVersionOption()

        self.cursorOption = QCommandLineOption(["m", "mouse-cursor"], "Maus anzeigen")
        self.parser.addOption(self.cursorOption)

        self.configOption = QCommandLineOption(["c", "config"], "Systemkonfiguration setzen")
        self.parser.addOption(self.configOption)

        self.loggingOption = QCommandLineOption(["log"], "Logging aktivieren", "level", "INFO")
        self.parser.addOption(self.loggingOption)

        self.parser.process(app)

    def is_mouse_cursor(self):
        return self.parser.isSet(self.cursorOption)

    def is_config_mode(self):
        return self.parser.isSet(self.configOption)
    
    def log_level(self):
        return self.parser.value(self.loggingOption).lower()

def start_gui(argv):
    log = logs.logger.add_module("start_gui")
    app = QApplication(argv)

    log.debug("Parser")
    parser = CliParser(app)

    log.debug("MainWindowB")
    mainWindow = MainWindowB()
    
    log.debug("Box")
    box = Box(mainWindow, parser.is_config_mode(), parser.log_level().upper())

    if not parser.is_mouse_cursor():
        # disable mouse-cursor
        log.debug("Set mouse")
        app.setOverrideCursor(Qt.BlankCursor)

    log.debug("Show screen")
    mainWindow.show()
    log.debug("Start")
    result = app.exec_()
    log.info("Terminate thread")
    box.thread.stop_thread()
    log.warning(str("End with result {}").format(result))
    return result


if __name__ == "__main__":
    result = start_gui(sys.argv)
    logging.critical("Result: %a", result)
    sys.exit(result)
