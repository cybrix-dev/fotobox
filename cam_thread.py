import const
import queue
import logs
from cam import Camera

from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal)

from enum import Enum

import logging
import time


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
    sig_error = pyqtSignal(object)
    sig_critical = pyqtSignal(int)

    def __init__(self, parent, expected_memory):
        self.log = logs.logger.add_module("Threading")
        QThread.__init__(self, parent)
        self.cam = Camera(expected_memory)
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
        self.log.debug("Start liveview")
        self.sendThreadCommand(Action.PREVIEW)

    def capture_image(self):
        '''
        Erstellt Foto. Daten werden via sig_foto gesendet
        '''
        self.log.debug("Capture image")
        self.sendThreadCommand(Action.CAPTURE)

    def get_available_space(self):
        return self.available_space

    def store_last(self, filename):
        self.log.debug("Store image")
        self.filename = filename
        self.sendThreadCommand(Action.STORE)

    def dismiss_last(self):
        self.log.debug("Delete image")
        self.sendThreadCommand(Action.DISMISS)

    def stop_thread(self):
        self.sendThreadCommand(Action.TERMINATE)
        while self.isRunning():
            self.yieldCurrentThread()
        self.log.info("Thread terminated")

    def run(self):
        self.log.info("Thread started")
        state = const.STATE_LIVE
        ts = 0
        while True:
            old_state = state
            if not self.cmd_fifo.empty():
                state = self.cmd_fifo.get()
                ts = time.time()

            if state == Action.PREVIEW:
                # kontinuierlich livebild abholen und an GUI senden
                self.sig_live_view.emit(self.cam.fetch_preview())
            elif state == Action.CAPTURE:
                # einmal Foto machen und an GUI senden
                # danach warten bis weiter
                photo = self.cam.capture_image()
                if self.cam.last_image:
                    self.sig_photo.emit(photo)
                else:
                    self.sig_error.emit(photo)
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
                # BUGFIX: wenn die Kamera 30min nicht verwendet wurde, schaltet sie sich automatisch aus.
                # wenn man mind. diese Zeit auf dem Auswahlbildschirm steht, stuerzt beim naechsten Kamerazugriff
                # die Applikation ab. Loesung: kontinuierlich alle x Sekunden preview von Kamera abholen,
                # Daten aber verwerfen
                if ((ts + 10) < time.time()):
                    ts = time.time()
                    self.cam.fetch_preview()
                else:
                    self.msleep(100)

            if self.cam.error_count > const.MAX_ERROR_COUNT:
                self.sig_critical.emit(self.cam.error_count)

if __name__ == "__main__":
    import sys
    logs.logger.change_level(logging.DEBUG)
    
    logging.info("QCoreApplication")
    app = QCoreApplication(sys.argv)
    logging.info("Threading()")
    thread = Threading(None, "SD")
    logging.info("finished.connect()")
    thread.finished.connect(app.exit)

    logging.info("thread.start_live()")
    thread.start_live()
    logging.info("thread.capture_image()")
    thread.capture_image()
    logging.info("thread.dismiss_last()")
    thread.dismiss_last()
    logging.info("thread.start_live()")
    thread.start_live()
    logging.info("thread.capture_image()")
    thread.capture_image()
    logging.info("thread.store_last(\"./test.jpg\")")
    thread.store_last("./test.jpg")
    logging.info("thread.start_live()")
    thread.start_live()
    logging.info("thread.stop_thread()")
    thread.stop_thread()

    logging.info("sys.exit(app.exec_())")
    sys.exit(app.exec_())
