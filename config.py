import const
import logs
from config_gui import Ui_Dialog as ui

from PyQt5.QtCore import pyqtSignal, Qt, QObject, QSettings  
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.Qt import QPixmap

import sys
import logging
from _operator import is_


def checkbox_style_sheet(size):
    checkBoxStyleSheet = "QCheckBox::indicator{open} width: {size}px; height: {size}px; {close}"
    #sliderStyleSheet = "QSlider::handle:horizontal{open} width: {width}px; height: {height}px; {close}"
    
    '''QSlider::handle:horizontal {
        background: #22B14C;
        border: 5px solid #B5E61D;
        width: 23px;
        height: 100px;
        margin: -24px -12px;
    }'''
    
    return str(checkBoxStyleSheet).format(size=size, open="{", close="}")

class Config(QObject):

    sig_finished = pyqtSignal()
    sig_reset = pyqtSignal()

    def __init__(self, parent, iniFilename, is_system):
        self.log = logs.logger.add_module("Config")
        self.log.debug("__init__(iniFilename=%a, is_system=%a)", iniFilename, is_system)
        if is_system:
            config_name = "system"
        else:
            config_name = "user"
        self.log.info("Start config with mode: %a", config_name)
        
        super().__init__(parent)
        
        self.dialog = QDialog(parent)
        self.ui = ui()
        self.ui.setupUi(self.dialog)

        self.system_config = is_system
        if is_system:
            self.ui.btReset.clicked.connect(self.slot_reset)
            self.ui.btDefaults.clicked.connect(self.slot_restore_defaults)
        else:                        
            self.ui.btReset.hide()
            self.ui.btDefaults.hide()
            self.ui.labCamSpaceType.hide()
            self.ui.labCamSpace.hide()
            self.ui.labCamSpaceIcon.hide()
            count = self.ui.tabWidget.count()
            for i in range(count-1, 0, -1):
                if self.ui.tabWidget.tabText(i) != "Anwender":
                    self.ui.tabWidget.removeTab(i)

        # increase size of checkbox to 40x40
        self.ui.ckImageFit.setStyleSheet(checkbox_style_sheet(const.CHECKBOX_SIZE))
        self.ui.ckImageMirrored.setStyleSheet(checkbox_style_sheet(const.CHECKBOX_SIZE))

        self.hide_gui()

        self.ui.slideCountdown.valueChanged.connect(self.slot_slide_countdown_changed)
        self.ui.slideTransparency.valueChanged.connect(self.slot_slide_transparency_changed)
        self.ui.spinCriticalMemory.valueChanged.connect(self.slot_critical_memory_value_changed)
        self.ui.spinLowMemory.valueChanged.connect(self.slot_low_memory_value_changed)
        self.ui.buttonBox.accepted.connect(self.slot_new_config)

        self.filename = iniFilename
        self.load_defaults()
        self.load_from_file()

    def set_space_icon(self, label, free_space):
        self.log.debug("set_space_icon: %a", free_space)
        if free_space <= self.critical_space:
            icon = QPixmap(const.IMG_ERR)
        elif free_space <= self.low_space:
            icon = QPixmap(const.IMG_WARN)
        else:
            icon = QPixmap(const.IMG_OK)
        
        label.setText("")
        # use a square of the height
        label.setPixmap(icon.scaled(label.height(),
                                    label.height(),
                                    Qt.KeepAspectRatio))

    def show_gui(self):
        self.log.info("show_gui")
        self.dialog.showFullScreen()

    def hide_gui(self):
        self.log.info("hide_gui")
        self.dialog.hide()
        
    def load_defaults(self):
        self.log.debug("load_defaults")
        # Anwender Tab
        self.trigger_opacity = 0.25
        self.countdown = 3  # countdown-timer in s - 3s
        self.image_resize_type = Qt.KeepAspectRatioByExpanding


        # System tab
        self.usb_root = "/media/pi"
        self.usb_path = "fotobox"
        self.usb_file_string = "%Y-%m-%d_%H-%M-%S.jpg"

        self.low_space = 100000  # in KB - 100MB
        self.critical_space = 10000  # in KB - 10MB
        self.bist_interval = 5000  # memcheck interval in ms - 5s

        self.camera_memory = "SD"
        self.image_mirrored = True

        # GUI tab
        self.knob_resize_factor = 1.0
        self.knob_icon_factor = 0.75


    def handle_config_file(self, load):
        self.log.debug("handle_config_file")
        '''
        Handles accessing the INI-file
        
        @param load: bool, marks if the content is loaded from file if set to True
                     or if the content is written to file if set to False
        '''
        settings = QSettings(self.filename, QSettings.IniFormat)

        def handle_value(name, value, user_parameter=False):
            if load:
                tmp_value = settings.value(name, value)
                value = type(value)(tmp_value)
            elif user_parameter or self.system_config:
                # always store user-parameters
                # only store system-parameters in system-mode 
                settings.setValue(name, str(value))
            return value
        
        settings.beginGroup("Global")
        self.low_space = handle_value("low_space", self.low_space)
        self.critical_space = handle_value("critical_space", self.critical_space)
        settings.endGroup()
                
        settings.beginGroup("GUI")
        self.image_mirrored = handle_value("image_mirrored", self.image_mirrored)
        self.knob_resize_factor = handle_value("knob_resize", self.knob_resize_factor)
        self.knob_icon_factor = handle_value("knob_icon", self.knob_icon_factor)
        self.trigger_opacity = handle_value("trigger_opacity", self.trigger_opacity, True)
        
        stretch_image = (self.image_resize_type == Qt.KeepAspectRatioByExpanding)
        stretch_image = handle_value("stretch_image", stretch_image, True)
        if stretch_image:
            self.image_resize_type = Qt.KeepAspectRatioByExpanding
        else:
            self.image_resize_type = Qt.KeepAspectRatio
        settings.endGroup()  # GUI

        settings.beginGroup("Camera")
        self.camera_memory = handle_value("memory_type", self.camera_memory)
        settings.endGroup()  # Camera

        settings.beginGroup("Timer")
        self.countdown = handle_value("countdown", self.countdown, True)
        self.bist_interval = handle_value("bist_interval", self.bist_interval)
        settings.endGroup()  # Timer

        settings.beginGroup("USB")
        self.usb_file_string = handle_value("filename", self.usb_file_string)
        self.usb_path = handle_value("path", self.usb_path)
        self.usb_root = handle_value("root", self.usb_root)  # byte-string
        settings.endGroup()  # USB

    def handle_gui(self, load):
        self.log.debug("handle_gui")
        def handle_text(line, text):
            if load:
                line.setText(text)
            else:
                text = line.text()
            return text

        self.usb_path = handle_text(self.ui.lineUsbPath, self.usb_path)
        self.usb_file_string = handle_text(self.ui.lineUsbFilename, self.usb_file_string)
        self.usb_root = handle_text(self.ui.lineUsbRoot, self.usb_root)

        def handle_value(spin, value):
            if load:
                spin.setValue(value)
            else:
                value = spin.value()
            return value

        self.countdown = handle_value(self.ui.slideCountdown, self.countdown)
        
        # low space internally in KB but config GUI in MB
        low_space_mb = self.low_space // 1000
        low_space_mb = handle_value(self.ui.spinLowMemory, low_space_mb)
        self.low_space = low_space_mb * 1000
        
        # critical space internally in KB but config GUI in MB
        critical_space_mb = self.critical_space // 1000
        critical_space_mb = handle_value(self.ui.spinCriticalMemory, critical_space_mb)
        self.critical_space = critical_space_mb * 1000
        
        self.bist_interval = handle_value(self.ui.spinBistInterval, self.bist_interval)
        self.knob_resize_factor = handle_value(self.ui.spinKnobResize, self.knob_resize_factor)
        self.knob_icon_factor = handle_value(self.ui.spinKnobIcon, self.knob_icon_factor)

        # on GUI: transparency / internally: opacity
        value = int((1 - self.trigger_opacity)*100)
        value = handle_value(self.ui.slideTransparency, value)
        self.trigger_opacity = 1 - value/100

        def handle_check(check, var):
            if load:
                check.setChecked(var)
            else:
                var = check.isChecked()
            return var

        self.image_mirrored = handle_check(self.ui.ckImageMirrored, self.image_mirrored)

        stretch_image = (self.image_resize_type == Qt.KeepAspectRatioByExpanding)
        stretch_image = handle_check(self.ui.ckImageFit, stretch_image)
        if stretch_image:
            self.image_resize_type = Qt.KeepAspectRatioByExpanding
        else:
            self.image_resize_type = Qt.KeepAspectRatio

        if load:
            self.ui.comboCameraMemory.setCurrentIndex(0)
            for i in range(0, self.ui.comboCameraMemory.count()):
                if self.ui.comboCameraMemory.itemText(i) == self.camera_memory:
                    self.ui.comboCameraMemory.setCurrentIndex(i)
                    break
        else:
            self.camera_memory = self.ui.comboCameraMemory.currentText()

    def load_from_file(self):
        self.log.info("load_from_file")
        self.handle_config_file(True)

    def store_to_file(self):
        self.log.info("store_to_file")
        self.handle_config_file(False)

    def open_config(self, usb_space, cam_space, cam_memory):
        self.log.info(str("open_config(usb_space={}, cam_space={}, cam_memory={})").format(usb_space, cam_space, cam_memory))

        # fill start-page
        self.ui.labUsbSpace.setText(str("{} MB").format(usb_space // 1000))
        self.set_space_icon(self.ui.labUsbSpaceIcon, usb_space)

        for item in cam_memory:
            self.ui.comboCameraMemory.addItem(item)
        
        if self.system_config:

            self.ui.labCamSpaceType.setText(str("Platz auf Kamera ({})").format(self.camera_memory))
            self.ui.labCamSpace.setText(str("{} MB").format(cam_space // 1000))
            self.set_space_icon(self.ui.labCamSpaceIcon, cam_space)
            
        # assign current config to GUI
        self.handle_gui(True)
        self.show_gui()

    def slot_slide_transparency_changed(self, value):
        self.ui.labTransparency.setText(str(value) + "%")
        self.trigger_opacity = 1 - (value / 100)

    def slot_slide_countdown_changed(self, value):
        self.ui.labCountdown.setText(str(value) + "s")

    def slot_low_memory_value_changed(self, value):
        if value < self.ui.spinCriticalMemory.value():
            self.ui.spinCriticalMemory.setValue(value)

    def slot_critical_memory_value_changed(self, value):
        if value > self.ui.spinLowMemory.value():
            self.ui.spinLowMemory.setValue(value)

    def slot_new_config(self):
        self.log.debug("slot_new_config")
        # assign all new values
        self.handle_gui(False)

        # store in INI-file
        self.store_to_file()

        # hide config-screen
        self.hide_gui()

        # trigger update in user-objects
        self.sig_finished.emit()

    def slot_reset(self):
        self.log.debug("slot_reset")
        self.slot_new_config()
        self.sig_reset.emit()
        
    def slot_restore_defaults(self):
        self.log.debug("slot_restore_defaults")
        self.load_defaults()
        self.handle_gui(True)


if __name__ == "__main__":
    logs.logger.change_level(logging.DEBUG)

    logging.info("QApplication()")
    app = QApplication(sys.argv)
    logging.info("QDialog()")
    MainWindow = QDialog()
    logging.info("Config(MainWindow, const.INI_FILE, True)")
    config = Config(MainWindow, const.INI_FILE, True)
    logging.info("config.open_config(50000,50000, ['SD', 'internal memory'])")
    config.open_config(50000,50000, ["SD", "internal memory"])
    logging.info("sys.exit(app.exec_())")
    
    config.ui.btReset.clicked.connect(config.ui.buttonBox.close)
    sys.exit(app.exec_())
