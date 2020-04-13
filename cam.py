from PyQt5.QtCore import *
import const
import queue
import logging
import gphoto2 as gp

class Camera(QThread):

    sig_live_view = pyqtSignal(object)
    sig_foto = pyqtSignal(object)

    def __init__(self):
        print("Camera.__init__()")
        logging.basicConfig(format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
        self.cmd_fifo = queue.Queue()

        gp.check_result(gp.use_python_logging())

        # copy+paste: gphoto2/examples/preview-image.py
        self.cam = gp.check_result(gp.gp_camera_new())
        gp.check_result(gp.gp_camera_init(self.cam))

        # required configuration will depend on camera type!
        print('Checking camera config')
        # get configuration tree
        config = gp.check_result(gp.gp_camera_get_config(self.cam))
        # find the image format config item
        # camera dependent - 'imageformat' is 'imagequality' on some
        OK, image_format = gp.gp_widget_get_child_by_name(config, 'imageformat')
        if OK >= gp.GP_OK:
            # get current setting
            value = gp.check_result(gp.gp_widget_get_value(image_format))
            # make sure it's not raw
            if 'raw' in value.lower():
                print('Cannot preview raw images')
                return 1
        # find the capture size class config item
        # need to set this on my Canon 350d to get preview to work at all
        OK, capture_size_class = gp.gp_widget_get_child_by_name( config, 'capturesizeclass')
        if OK >= gp.GP_OK:
            # set value
            value = gp.check_result(gp.gp_widget_get_choice(capture_size_class, 2))
            gp.check_result(gp.gp_widget_set_value(capture_size_class, value))
            # set config
            gp.check_result(gp.gp_camera_set_config(self.cam, config))


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

    def fetch_preview(self):
        '''
        Holt ein einzelnes Vorschaubild von der Kamera
        '''
        # capture preview image (not saved to camera memory card)
        print('Capturing preview image')
        camera_file = gp.check_result(gp.gp_camera_capture_preview(self.cam))
        file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))
        # camera_file = self._cap.capture_preview()
        # file_data = camera_file.get_data_and_size()
        # return Image.open(io.BytesIO(file_data))
        return QPixmap(io.BytesIO(file_data))

    def run(self):
        state = const.STATE_LIVE
        while True:
            if not self.cmd_fifo.empty():
                state = self.cmd_fifo.get()

            if state == const.STATE_LIVE:
                '''
                picture = self.fetch_preview()
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