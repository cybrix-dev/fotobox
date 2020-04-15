from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
import logging

try:
    import gphoto2 as gp
except:
    debug = 1
else:
    debug = 0


class Camera:

    def __init__(self):
        print('debug: ', debug)
        logging.basicConfig(format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
        if debug == 1:
            self.index = 0
        else:
            # copy+paste: gphoto2/examples/preview-image.py
            gp.check_result(gp.use_python_logging())

            self.cam = gp.check_result(gp.gpself.camera_new())
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

    def fetch_preview(self):
        '''
        Holt ein einzelnes Vorschaubild von der Kamera
        '''
        if debug == 1:
            self.index += 1
            if (self.index % 2) == 0:
                file = './icons/test1.jpg'
            else:
                file = './icons/test2.jpg'
            return QPixmap(file)
        else:
            # capture preview image (not saved to camera memory card)
            print('Capturing preview image')
            camera_file = gp.check_result(gp.gp_camera_capture_preview(self.cam))
            file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))
            # camera_file = self._cap.capture_preview()
            # file_data = camera_file.get_data_and_size()
            # return Image.open(io.BytesIO(file_data))

            # return QPixmap().loadFromData(io.BytesIO(file_data).getvalue())
            result = QPixmap()
            result.loadFromData(file_data)
            return result
