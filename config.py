import const
from config_gui import Ui_Dialog as ui

from PyQt5.QtCore import pyqtSignal, Qt, QObject, QSettings  
from PyQt5.QtWidgets import QDialog, QApplication

import sys


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
    
    return str(checkBoxStyleSheet).format(size=40, open="{", close="}")

class Config(QObject):

    sig_finished = pyqtSignal()
    sig_reset = pyqtSignal()

    def __init__(self, parent, iniFilename, isSystem, camMemory=["SD"]):
        super().__init__(parent)

        self.dialog = QDialog(parent)
        self.ui = ui()
        self.ui.setupUi(self.dialog)

        if not isSystem:
            self.ui.btReset.hide()
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
        self.ui.buttonBox.accepted.connect(self.slot_new_config)
        self.ui.btReset.clicked.connect(self.slot_reset)

        for item in camMemory:
            self.ui.comboCameraMemory.addItem(item)

        self.filename = iniFilename
        self.load_defaults()
        self.load_from_file()

    def show_gui(self):
        self.dialog.showFullScreen()

    def hide_gui(self):
        self.dialog.hide()
        
    def load_defaults(self):
        # Anwender Tab
        self.trigger_opacity = 0.25
        self.countdown = 3  # countdown-timer in s - 3s
        self.image_resize_type = Qt.KeepAspectRatioByExpanding


        # System tab
        self.usb_root = "/media/pi"
        self.usb_path = "fotobox"
        self.usb_file_string = "%Y-%m-%d_%H-%M-%S.jpg"

        self.critical_space = 100000  # in KB - 100MB
        self.bist_interval = 5000  # memcheck interval in ms - 5s

        self.camera_memory = "SD"
        self.image_mirrored = True

        # GUI tab
        self.knob_resize_factor = 1.0
        self.knob_icon_factor = 0.75


    def handle_config_file(self, load):
        '''
        Handles accessing the INI-file
        
        @param load: bool, marks if the content is loaded from file if set to True
                     or if the content is written to file if set to False
        '''
        settings = QSettings(self.filename, QSettings.IniFormat)

        def handle_value(settings, name, value, load):
            if load:
                tmp_value = settings.value(name, value)
                value = type(value)(tmp_value)
            else:
                settings.setValue(name, str(value))
            return value
        
        settings.beginGroup("General")
        self.critical_space = handle_value(settings, "critical_space", self.critical_space, load)
        settings.endGroup()  # General
                
        settings.beginGroup("GUI")
        self.image_mirrored = handle_value(settings, "image_mirrored", self.image_mirrored, load)
        self.knob_resize_factor = handle_value(settings, "knob_resize", self.knob_resize_factor, load)
        self.knob_icon_factor = handle_value(settings, "knob_icon", self.knob_icon_factor, load)
        self.trigger_opacity = handle_value(settings, "trigger_opacity", self.trigger_opacity, load)
        
        stretch_image = (self.image_resize_type == Qt.KeepAspectRatioByExpanding)
        stretch_image = handle_value(settings, "stretch_image", stretch_image, load)
        if stretch_image:
            self.image_resize_type = Qt.KeepAspectRatioByExpanding
        else:
            self.image_resize_type = Qt.KeepAspectRatio
        settings.endGroup()  # GUI

        settings.beginGroup("Camera")
        self.camera_memory = handle_value(settings, "memory_type", self.camera_memory, load)
        settings.endGroup()  # Camera

        settings.beginGroup("Timer")
        self.countdown = handle_value(settings, "countdown", self.countdown, load)
        self.bist_interval = handle_value(settings, "bist_interval", self.bist_interval, load)
        settings.endGroup()  # Timer

        settings.beginGroup("USB")
        self.usb_file_string = handle_value(settings, "filename", self.usb_file_string, load)
        self.usb_path = handle_value(settings, "path", self.usb_path, load)
        self.usb_root = handle_value(settings, "root", self.usb_root, load)  # byte-string
        settings.endGroup()  # USB

    def handle_gui(self, load):
        def handle_text(line, text, load):
            if load:
                line.setText(text)
            else:
                text = line.text()
            return text

        self.usb_path = handle_text(self.ui.lineUsbPath, self.usb_path, load)
        self.usb_file_string = handle_text(self.ui.lineUsbFilename, self.usb_file_string, load)
        self.usb_root = handle_text(self.ui.lineUsbRoot, self.usb_root, load)

        def handle_value(spin, value, load):
            if load:
                spin.setValue(value)
            else:
                value = spin.value()
            return value

        self.countdown = handle_value(self.ui.slideCountdown, self.countdown, load)
        
        # critical space internally in KB but config GUI in MB
        critical_space_mb = self.critical_space // 1000
        critical_space_mb = handle_value(self.ui.spinCriticalMemory, critical_space_mb, load)
        self.critical_space = critical_space_mb * 1000
        
        self.bist_interval = handle_value(self.ui.spinBistInterval, self.bist_interval, load)
        self.knob_resize_factor = handle_value(self.ui.spinKnobResize, self.knob_resize_factor, load)
        self.knob_icon_factor = handle_value(self.ui.spinKnobIcon, self.knob_icon_factor, load)

        # on GUI: transparency / internally: opacity
        value = int((1 - self.trigger_opacity)*100)
        value = handle_value(self.ui.slideTransparency, value, load)
        self.trigger_opacity = 1 - value/100

        def handle_check(check, var, load):
            if load:
                check.setChecked(var)
            else:
                var = check.isChecked()
            return var

        self.image_mirrored = handle_check(self.ui.ckImageMirrored, self.image_mirrored, load)

        stretch_image = (self.image_resize_type == Qt.KeepAspectRatioByExpanding)
        stretch_image = handle_check(self.ui.ckImageFit, stretch_image, load)
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
        self.handle_config_file(True)

    def store_to_file(self):
        self.handle_config_file(False)

    def open_config(self):
        # assign current config to GUI
        self.handle_gui(True)
        self.show_gui()

    def slot_slide_transparency_changed(self, value):
        self.ui.labTransparency.setText(str(value) + "%")
        self.trigger_opacity = 1 - (value / 100)

    def slot_slide_countdown_changed(self, value):
        self.ui.labCountdown.setText(str(value) + "s")

    def slot_new_config(self):
        # assign all new values
        self.handle_gui(False)

        # store in INI-file
        self.store_to_file()

        # hide config-screen
        self.hide_gui()

        # trigger update in user-objects
        self.sig_finished.emit()


    def slot_reset(self):
        self.store_to_file()
        self.sig_reset.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QDialog()
    config = Config(MainWindow, const.INI_FILE, True)
    config.open_config()
    sys.exit(app.exec_())
