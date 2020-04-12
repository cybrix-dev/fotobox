from PyQt5.QtCore import *
import const
import queue
import gphoto2 as gp

class Camera(QThread):

    sig_live_view = pyqtSignal(object)
    sig_foto = pyqtSignal(object)

    def __init__(self):
        self.cmd_fifo = queue.Queue()
        self.cam = gp.

    def start_live(self):
        '''
        Startet die Vorschau. Daten werden via sig_live_view gesendet
        '''
        self.cmd_fifo.put(const.STATE_LIVE)

    def capture_image(self):
        '''
        Erstellt Foto. Daten werden via sig_foto gesendet
        '''
        self.cmd_fifo.put(const.STATE_BILD)

    def run(self):
        state = const.STATE_LIVE
        while True:
            if not self.cmd_fifo.empty():
                state = self.cmd_fifo.get()

            if state == const.STATE_LIVE:
                '''
                camera_file = self._cap.capture_preview()
                file_data = camera_file.get_data_and_size()
                return Image.open(io.BytesIO(file_data))
                ---
                if self._rotation is not None:
                    picture = picture.transpose(self._rotation)
                picture = picture.resize(self._pic_dims.previewSize)
                picture = ImageOps.mirror(picture)
                byte_data = BytesIO()
                picture.save(byte_data, format='jpeg')
                '''
            elif state == const.STATE_BILD:
                '''
                file_path = self._cap.capture(gp.GP_CAPTURE_IMAGE)
                camera_file = self._cap.file_get(file_path.folder, file_path.name,
                                                 gp.GP_FILE_TYPE_NORMAL)
                file_data = camera_file.get_data_and_size()
                return Image.open(io.BytesIO(file_data))
                '''