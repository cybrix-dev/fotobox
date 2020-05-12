'''
Created on 11.05.2020

@author: Seoman303
'''
import logging
import const

class Logger:
    def __init__(self, log_level=logging.INFO):
        self.logger = []
        self.log_level = log_level
        const.setup_logs(log_level)

        log = self.add_module("Logger")

        self.change_level(log_level)
        log.critical("Start")
#         
#     def add_module(self, log):
#         log.addHandler(self.streamer)
        
    def change_level(self, log_level):
        self.log_level = log_level
        for mod in self.logger:
            mod.setLevel(log_level)

#         logging.setLevel(log_level)
    def add_module(self, name):
        result = logging.getLogger(name)
        result.setLevel(self.log_level)
        self.logger.append(result)
        return result


logger = Logger()