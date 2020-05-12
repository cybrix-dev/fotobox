import logging
import time
from logs import logger 

try:
    import gphoto2 as gp
except:
    import io
    import const

    debug = True
else:
    debug = False

'''
Indices in available memory-tuple
'''
MEM_NAME = 0
MEM_SPACE_LEFT = 1
MEM_INDEX = 2

class Camera:

    def __init__(self, memory_type=None):
        self.log = logger.add_module("Camera")
        
        if debug:
            self.log.info('debug mode without actual camera')

        self.last_image = False
        self.memory_type = memory_type
        self.last_image = None
        
        self.last_success = False
        self.error_count = 0
        self.global_errors = 0
        
        if debug:
            self.index = 0
        else:
            # copy+paste: gphoto2/examples/preview-image.py
            gp.check_result(gp.use_python_logging())

            self.cam = gp.check_result(gp.gp_camera_new())
            gp.check_result(gp.gp_camera_init(self.cam))

            # required configuration will depend on camera type!
            # get configuration tree
            config = gp.check_result(gp.gp_camera_get_config(self.cam))
            
        self.available_memory = []
        self.load_available_memory(True)
        
        #now comes the configuration which depends on the camera used
        if not debug:
            # find the image format config item
            # camera dependent - 'imageformat' is 'imagequality' on some
            OK, image_format = gp.gp_widget_get_child_by_name(config, 'imageformat')
            if OK >= gp.GP_OK:
                # get current setting
                value = gp.check_result(gp.gp_widget_get_value(image_format))
                # make sure it's not raw
                if 'raw' in value.lower():
                    self.log.error('Cannot preview raw images')
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
                
            # set storage folder+file - TODO: depending on memory_type
            capture_target = 1
            for mem in self.available_memory:
                if mem[MEM_NAME] == memory_type:
                    capture_target = mem[MEM_INDEX]
                    break
                
            OK, capture_target_class = gp.gp_widget_get_child_by_name( config, 'capturetarget')
            if OK >= gp.GP_OK:
                # set value
                value = gp.check_result(gp.gp_widget_get_choice(capture_target_class, capture_target))
                gp.check_result(gp.gp_widget_set_value(capture_target_class, value))
                # set config
                gp.check_result(gp.gp_camera_set_config(self.cam, config))
                
    def check_success(self, result, name, reset_counter=False):
        if not debug:
            '''
            Modified copy from gphoto2/result.py
            '''
            if not isinstance(result, (tuple, list)):
                error = result
            elif len(result) == 2:
                error, result = result
            else:
                error = result[0]
                result = result[1:]
                
            if error >= gp.GP_OK:
                self.last_success = True
                if reset_counter:
                    self.error_count = 0
            else:
                self.last_success = False
                self.error_count += 1
                self.global_errors += 1
                self.log.error(str("{} failed with {} - Errors in a row: {} / Errors since start: {}")
                               .format(name, gp.gp_result_as_string(error), self.error_count, self.global_errors))
            return result

    def set_memory_type(self, memory_type):
        # TODO: update destination-memory
        self.memory_type = memory_type

    def prepare_pixmap(self,camera_file):
        return self.check_success(gp.gp_file_get_data_and_size(camera_file), "gp_file_get_data_and_size")

    def fetch_preview(self):
        '''
        Holt ein einzelnes Vorschaubild von der Kamera
        '''
        if debug:
            self.index += 1
            time.sleep(0.2)
            if (self.index % 3) == 0:
                file = const.IMG_PATH + '/test1.jpg'
            elif (self.index % 3) == 1:
                file = const.IMG_PATH + '/test2.jpg'    
            else:
                file = const.IMG_PATH + '/test3.jpg'
            return io.FileIO(file).read()
        else:
            next_image = self.check_success(gp.gp_camera_capture_preview(self.cam), "Preview", True)
            if self.last_success:
                self.last_image = next_image
                
            # capture preview image (not saved to camera memory card)
            return self.prepare_pixmap(self.last_image)

    def capture_image(self):
        self.last_image = True
        if debug:
            result = io.FileIO(const.IMG_PATH + '/test4.jpg').read()
        else:
            self.file_path = self.check_success(gp.gp_camera_capture(self.cam, gp.GP_CAPTURE_IMAGE), "Capture")
            if self.last_success:
                camera_file = self.check_success(gp.gp_camera_file_get(self.cam,
                                                    self.file_path.folder,
                                                    self.file_path.name,
                                                    gp.GP_FILE_TYPE_NORMAL), "camera_file_get")
                if self.last_success:
                    result = camera_file.get_data_and_size()
                    
            if not self.last_success:
                self.last_image = False
                result = self.fetch_preview()
                
        return result

    def dismiss_last(self):
        if self.last_image:
            if debug:
                self.log.debug("Dismiss last image")
            else:
                self.check_success(gp.gp_camera_file_delete(self.cam,
                                            self.file_path.folder,
                                            self.file_path.name),
                                   "camera_file_delete")

            self.last_image = False

    def store_last(self,dest):
        if self.last_image:
            if debug:
                self.log.debug("Store last image on USB: " + dest)
            else:
                camera_file = self.check_success(gp.gp_camera_file_get(self.cam,
                                                    self.file_path.folder,
                                                    self.file_path.name,
                                                    gp.GP_FILE_TYPE_NORMAL), "gp_camera_file_get")
                if self.last_success:
                    self.check_success(gp.gp_file_save(camera_file, dest), "gp_file_save")
                    if self.last_success:
                        self.log.debug("File stored: " + dest)
            self.last_image = False

    def print_mem_device(self, mem):
        self.log.info(str("description:   {}").format(mem.description))
        self.log.info(str("basedir:       {}").format(mem.basedir))
        self.log.info(str("label:         {}").format(mem.label))
        self.log.info(str("type:          {}").format(mem.type))
        self.log.info(str("fstype:        {}").format(mem.fstype))
        self.log.info(str("access:        {}").format(mem.access))
        self.log.info(str("capacitykbytes:{}").format(mem.capacitykbytes))
        self.log.info(str("freekbytes:    {}").format(mem.freekbytes))
        self.log.info(str("freeimages:    {}").format(mem.freeimages))
        self.log.info(str("fields:        {}").format(mem.fields))

    def get_available_space(self):
        result = -1
        for mem in self.available_memory:
            if mem[MEM_NAME] == self.memory_type:
                result = mem[MEM_SPACE_LEFT]
                break
                
        return result
    
    def load_available_memory(self, print_info=False):
        if debug:
            result = [("SD", 50000, 1)]
        else:
            result = []
            idx = 1
            arr = self.check_success(gp.gp_camera_get_storageinfo(self.cam), "gp_camera_get_storageinfo")
            for mem in arr:
                if print_info:
                    self.print_mem_device(mem)
                result.append((mem.description, mem.freekbytes, idx))
                idx += 1
                
        self.available_memory = result
            
        
if __name__ == "__main__":
    logger.change_level(logging.DEBUG)
    cam = Camera("SD")
    
    logging.info("cam.available_memory: %a", cam.available_memory)
    logging.info("cam.get_available_space(): %a", cam.get_available_space())
    
    logging.info("cam.capture_image()")
    cam.capture_image()
    logging.info("cam.dismiss_last()")
    cam.dismiss_last()
    logging.info("cam.capture_image()")
    cam.capture_image()
    logging.info("cam.store_last()")
    cam.store_last("./test0.jpg")
