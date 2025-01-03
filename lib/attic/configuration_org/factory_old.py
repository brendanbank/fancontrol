import sys
sys.path.append('/Users/brendan/src/fancontrol/lib')
import logging
import os

log = logging.getLogger(__name__)

CONFIGURATION_DIR = "lib/uconfiguration/items"

class ItemBase:
    _priority = 255
    config_attribute = False
    config_name = None
    
    def __init__(self, application_configuration, item_configuration):
            self.item_configuration =  item_configuration
            self.application_configuration = application_configuration
            
    @classmethod
    def configuration_name(cls):
        return(cls.config_name)

class ItemFactory:
    
    def __init__(self):
        self._configuration_classes = dict()
        self._register()

    def _register(self):
        
        for fiel in os.listdir(CONFIGURATION_DIR):                               
            if fiel.find(".py", len(fiel) -3, len(fiel)) > 0:
                name = fiel.replace(".py", "")
                
                items_location = ".".join(__name__.split('.')[:-1]) + '.items'                
                
                pkg_name = f'{items_location}.{name}'
                
                log.info (f'import {pkg_name}')
                __import__(pkg_name)

                module_obj = sys.modules[pkg_name]
                
                for item in dir(module_obj):
                    obj = getattr(module_obj,item)
                    if (str(type(obj)) == str(type)) :
                        if issubclass(obj, ItemBase) and obj != ItemBase:
                            self._configuration_classes[obj.configuration_name()] = obj

        

        log.debug(f'loaded uconfiguration classes {self._configuration_classes}')

    def get_objs(self):
        return(self._configuration_classes)

    def get(self, name):
        if name in self._configuration_classes.keys():
            return(self._configuration_classes[name])
        else:
            return(None)

