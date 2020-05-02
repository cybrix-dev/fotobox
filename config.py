import const
from config_gui import Ui_Dialog as ui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

checkBoxStyleSheet = \
    ("QCheckBox::indicator{open} width: {size}px; height: {size}px; {close} "
     "QCheckBox::indicator:checked{open} image: url({img_on}); {close}    "
     "QCheckBox::indicator:unchecked{open} image: url({img_off}); {close}  "
    )

class Config(QObject):

    sig_finished = pyqtSignal()

    def __init__(self, parent, iniFilename, isSystem):
        super().__init__(parent)

        self.dialog = QDialog(parent)
        self.ui = ui()
        self.ui.setupUi(self.dialog)
        self.ui.tabWidget.setTabEnabled(1, isSystem)
        stylesheet = str(checkBoxStyleSheet).format(size = 40, open = "{", close = "}", img_on = const.IMG_CK_ON, img_off = const.IMG_CK_OFF)
        print(stylesheet)
        self.ui.ckImageFit.setStyleSheet(stylesheet)
        self.hide_gui()

        self.ui.slideCountdown.valueChanged.connect(self.slot_slide_countdown_changed)
        self.ui.slideTransparency.valueChanged.connect(self.slot_slide_transparency_changed)
        self.ui.buttonBox.accepted.connect(self.slot_new_config)

        self.filename = iniFilename
        self.load_defaults()
        self.config_available = True  # TODO: use INI-file
        
    def show_gui(self):
        self.dialog.showFullScreen()

    def hide_gui(self):
        self.dialog.hide()
        
    def load_defaults(self):
        self.knob_resize_factor = 1
        self.knob_icon_factor = 0.75
        self.trigger_transparency = 0.25

        self.image_resize_type = Qt.KeepAspectRatioByExpanding
        self.image_mirrored = True

        self.critical_space = 100000  # in KB - 100MB

        self.countdown = 3  # countdown-timer in s - 3s
        self.bist_interval = 5000  # memcheck interval in ms - 5s

        self.usb_root = b"/media/pi"
        self.usb_path = "photobox"
        self.usb_file_string = "%Y-%m-%d_%H-%M-%S.jpg"
        
        self.camera_memory = "SD"

    def handle_config_file(self, load):
        settings = QSettings(self.filename)

        settings.beginGroup("GUI")
        settings.endGroup()

        settings.beginGroup("Image")
        settings.endGroup()

        settings.beginGroup("Camera")
        settings.endGroup()

        settings.beginGroup("Timer")
        settings.endGroup()

        settings.beginGroup("USB")
        settings.endGroup()

    def handle_gui(self, load):
        if load:
            # load the current values into GUI
            self.ui.slideCountdown.setValue(self.countdown)
            self.ui.slideTransparency.setValue(int((1 - self.trigger_transparency)*100))

            # checked: zoom-in for perfect fit
            isChecked = (self.image_resize_type == Qt.KeepAspectRatioByExpanding)
            self.ui.ckImageFit.setChecked(isChecked)

        else:
            if self.ui.ckImageFit.isChecked():
                self.image_resize_type = Qt.KeepAspectRatioByExpanding
            else:
                self.image_resize_type = Qt.KeepAspectRatio

            self.countdown = self.ui.slideCountdown.value()
            self.trigger_transparency = 1 - (self.ui.slideTransparency.value()/100)

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
        self.trigger_transparency = 1 - (value / 100)

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


if __name__ == "__main__":
    import sys
    import const

    app = QApplication(sys.argv)
    MainWindow = QDialog()
    config = Config(MainWindow, const.INI_FILE, True)
    config.open_config()
    sys.exit(app.exec_())
