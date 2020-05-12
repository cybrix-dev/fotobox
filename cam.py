import logging
import time

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
        if debug:
            print('debug')
            
        print(time.strftime("Preview error: %H-%M-%S"))
        logging.basicConfig(format='%(levelname)s: %(name)s: %(message)s', level=logging.INFO)
        self.last_image = False
        self.memory_type = memory_type
        self.last_image = None
        self.is_error = False
        
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

    def set_memory_type(self, memory_type):
        # TODO: update destination-memory
        self.memory_type = memory_type

    def prepare_pixmap(self,camera_file):
        return gp.check_result(gp.gp_file_get_data_and_size(camera_file))

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
            self.is_error = False
            try:
                self.last_image = gp.check_result(gp.gp_camera_capture_preview(self.cam))
            except:
                '''
                mark error
                '''
                print(time.strftime("Preview error: %H-%M-%S"))
                self.is_error = True
                
            # capture preview image (not saved to camera memory card)
            return self.prepare_pixmap(self.last_image)

    def capture_image(self):
        self.last_image = True
        if debug:
            result = io.FileIO(const.IMG_PATH + '/test4.jpg').read()
        else:
            try:
                self.file_path = gp.check_result(gp.gp_camera_capture(self.cam, gp.GP_CAPTURE_IMAGE))
                camera_file = gp.check_result(gp.gp_camera_file_get(self.cam,
                                                    self.file_path.folder,
                                                    self.file_path.name,
                                                    gp.GP_FILE_TYPE_NORMAL))

                result = camera_file.get_data_and_size()
            except:
                self.last_image = False
                result = self.fetch_preview()
                
        return result

    def dismiss_last(self):
        if self.last_image:
            if debug:
                print("Dismiss last image")
            else:
                gp.check_result(gp.gp_camera_file_delete(self.cam,
                                        self.file_path.folder,
                                        self.file_path.name))
            self.last_image = False

    def store_last(self,dest):
        if self.last_image:
            if debug:
                print("Store last image on USB: ", dest)
            else:
                camera_file = gp.check_result(gp.gp_camera_file_get(self.cam,
                                                    self.file_path.folder,
                                                    self.file_path.name,
                                                    gp.GP_FILE_TYPE_NORMAL))
                gp.check_result(gp.gp_file_save( camera_file, dest ))
            self.last_image = False

    def print_mem_device(self, mem):
        print("description:   ", mem.description)
        print("basedir:       ", mem.basedir)
        print("label:         ", mem.label)
        print("type:          ", mem.type)
        print("fstype:        ", mem.fstype)
        print("access:        ", mem.access)
        print("capacitykbytes:", mem.capacitykbytes)
        print("freekbytes:    ", mem.freekbytes)
        print("freeimages:    ", mem.freeimages)
        print("fields:        ", mem.fields)

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
            arr = gp.check_result(gp.gp_camera_get_storageinfo(self.cam))
            for mem in arr:
                if print_info:
                    self.print_mem_device(mem)
                result.append((mem.description, mem.freekbytes, idx))
                idx += 1
                
        self.available_memory = result
            

        
if __name__ == "__main__":
    cam = Camera("SD")
    
    print(cam.available_memory)
    print(cam.get_available_space())
    
    cam.capture_image()
    cam.dismiss_last()
    cam.capture_image()
    cam.store_last("./test0.jpg")
    
    