import const
import queue
from cam import Camera
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal)
from enum import Enum


class Action(Enum):
    NONE = 0
    PREVIEW = 1
    CAPTURE = 2
    STORE = 3
    DISMISS = 4

    TERMINATE = -1  # only for debugging


class Threading(QThread):

    sig_live_view = pyqtSignal(object)
    sig_photo = pyqtSignal(object)

    def __init__(self, parent):
        QThread.__init__(self, parent)
        self.cam = Camera()
        self.cmd_fifo = queue.Queue()
        self.available_space = self.cam.get_available_space()
        self.filename = ""

    def sendThreadCommand(self,cmd):
        if not self.isRunning():
            self.start()
        self.cmd_fifo.put(cmd)

    def start_live(self):
        '''
        Startet die Vorschau. Daten werden via sig_live_view gesendet
        '''
        self.sendThreadCommand(Action.PREVIEW)

    def capture_image(self):
        '''
        Erstellt Foto. Daten werden via sig_foto gesendet
        '''
        self.sendThreadCommand(Action.CAPTURE)

    def get_available_space(self):
        return self.available_space

    def store_last(self, filename):
        self.filename = filename
        self.sendThreadCommand(Action.STORE)

    def dismiss_last(self):
        self.sendThreadCommand(Action.DISMISS)

    def stop_thread(self):
        self.sendThreadCommand(Action.TERMINATE)

    def run(self):
        state = const.STATE_LIVE
        while True:
            old_state = state
            if not self.cmd_fifo.empty():
                state = self.cmd_fifo.get()

            if state == Action.PREVIEW:
                # kontinuierlich livebild abholen und an GUI senden
                self.sig_live_view.emit(self.cam.fetch_preview())
            elif state == Action.CAPTURE:
                # einmal Foto machen und an GUI senden
                # danach warten bis weiter
                self.sig_photo.emit(self.cam.capture_image())
                self.available_space = self.cam.get_available_space()
                state = Action.NONE
            elif state == Action.STORE:
                self.cam.store_last(self.filename)
                state = old_state
            elif state == Action.DISMISS:
                self.cam.dismiss_last()
                state = old_state
            elif state == Action.TERMINATE:
                return
            else:
                # nichts machen, um CPU zu schonen, Pause
                self.msleep(100)


if __name__ == "__main__":
    import sys
    app = QCoreApplication(sys.argv)
    thread = Threading(None)
    thread.finished.connect(app.exit)

    thread.start_live()
    thread.capture_image()
    thread.dismiss_last()
    thread.start_live()
    thread.capture_image()
    thread.store_last("./test.jpg")
    thread.start_live()
    thread.stop_thread()

    sys.exit(app.exec_())
