import const
from PyQt5.QtCore import Qt

class Config:
    def __init__(self):

        self.config_available = True  # TODO: use INI-file

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

