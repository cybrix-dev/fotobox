from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
import logging

try:
    import gphoto2 as gp
except:
    import time
    debug = True
else:
    debug = False


class Camera:

    def __init__(self):
        print('debug: ', debug)
        logging.basicConfig(format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
        self.last_image = False
        if debug:
            self.index = 0
        else:
            # copy+paste: gphoto2/examples/preview-image.py
            gp.check_result(gp.use_python_logging())

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

    def prepare_pixmap(self,camera_file):
        file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))

        result = QPixmap()
        result.loadFromData(file_data)
        return result

    def fetch_preview(self):
        '''
        Holt ein einzelnes Vorschaubild von der Kamera
        '''
        if debug:
            self.index += 1
            time.sleep(0.05)
            if (self.index % 2) == 0:
                file = './icons/test1.jpg'
            else:
                file = './icons/test2.jpg'
            return QPixmap(file)
        else:
            # capture preview image (not saved to camera memory card)
            return self.prepare_pixmap( gp.check_result(gp.gp_camera_capture_preview(self.cam)))

    def capture_image(self):
        self.last_image = True
        if debug:
            return QPixmap('./icons/test3.jpg')
        else:
            self.file_path = gp.check_result(gp.gp_camera_capture(self.cam, gp.GP_CAPTURE_IMAGE))
            camera_file = gp.check_result(gp.gp_camera_file_get(self.cam,
                                                self.file_path.folder,
                                                self.file_path.name,
                                                gp.GP_FILE_TYPE_NORMAL))

            file_data = camera_file.get_data_and_size()
            result = QPixmap()
            result.loadFromData(file_data)
            return result

    def dismiss_last(self):
        if self.last_image:
            if debug:
                print("Dismiss last image")
            else:
                ''''''
                gp.check_result(gp.gp_camera_file_delete(self.cam,
                                        self.file_path.folder,
                                        self.file_path.name,
                                        gp.GP_FILE_TYPE_NORMAL))
            self.last_image = False

    def store_last(self,path):
        if self.last_image:
            if debug:
                print("Store last image on USB: ", path)
            else:
                '''
                
                '''
                
            self.last_image = False

    def get_available_space(self):
        if debug:
            return 50000000
        else:
            result = -1
            arr = gp.check_result(gp.gp_camera_get_storageinfo(self.cam))
            for mem in arr:
                if mem.description == "SD":
                    result = mem.freekbytes
                    break
                
            return result
            
        
if __name__ == "__main__":
    cam = Camera()
    print(cam.get_available_space())