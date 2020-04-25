import const
import queue
from cam import Camera
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal)


class Threading(QThread):

    sig_live_view = pyqtSignal(object)
    sig_photo = pyqtSignal(object)

    def __init__(self,parent,cam):
        QThread.__init__(self,parent)
        self.cam = cam
        self.cmd_fifo = queue.Queue()

    def sendThreadCommand(self,cmd):
        if not self.isRunning():
            self.start()
        self.cmd_fifo.put(cmd)

    def start_live(self):
        '''
        Startet die Vorschau. Daten werden via sig_live_view gesendet
        '''
        self.sendThreadCommand(const.STATE_LIVE)

    def capture_image(self):
        '''
        Erstellt Foto. Daten werden via sig_foto gesendet
        '''
        self.sendThreadCommand(const.STATE_BILD)

    def run(self):
        state = const.STATE_LIVE
        while True:
            if not self.cmd_fifo.empty():
                state = self.cmd_fifo.get()

            if state == const.STATE_LIVE:
                # kontinuierlich livebild abholen und an GUI senden
                self.sig_live_view.emit(self.cam.fetch_preview())
            elif state == const.STATE_BILD:
                # einmal Foto machen und an GUI senden
                # danach warten bis weiter
                self.sig_photo.emit(self.cam.capture_image())
                self.cam.get_available_space_int()
                state = const.STATE_IDLE
            else:
                # nichts machen, um CPU zu schonen, Pause
                self.msleep(100)


if __name__ == "__main__":
    import sys
    app = QCoreApplication(sys.argv)
    thread = Threading(None)
    thread.finished.connect(app.exit)
    sys.exit(app.exec_())
