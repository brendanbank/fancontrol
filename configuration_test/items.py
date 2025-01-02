import os, sys

import logging
log = logging.getLogger(__name__)


class BaseItem:
    _priority = 255
    item_name = None
    form = None
    
    def __init__(self, application_configuration, item_configuration):
            self.item_configuration =  item_configuration
            self.application_configuration = application_configuration        
        
    @classmethod
    def factory_configuration_name(cls):
        return(cls.item_name)
    


class ItemFactory:
    def __init__(self, item_directory, config):
        self._configuration_classes = dict()
        self.item_directory = item_directory
        self._list = list ()
        self._config_items = {}
        self.config = config
        self._register()
        self.factory_to_obj()
        
    def _register(self):
        if self.item_directory:
            all_configuration_classes = list()
            log.debug(f'try to read from directory {self.item_directory}')
            for fiel in os.listdir(self.item_directory):                               
                if fiel.endswith(".py"):
                    name = fiel.replace(".py", "")
                    items_location = ".".join(self.item_directory.split('/'))                
                    pkg_name = f'{items_location}.{name}'
                    
                    log.info (f'import {pkg_name}')
                    __import__(pkg_name)

                    module_obj = sys.modules[pkg_name]
                    
                    for item in dir(module_obj):
                        cls = getattr(module_obj,item)
                        if (str(type(cls)) == str(type)) :
                            if issubclass(cls, BaseItem) and cls != BaseItem:
                                self._configuration_classes[cls.factory_configuration_name()] = cls
                                all_configuration_classes.append(cls)

            
            self._list = sorted(all_configuration_classes, key=lambda k: k._priority)
            log.debug(f'loaded uconfiguration classes {self._configuration_classes}')
        else:
            log.debug(f'no uconfiguration classes directory configured')


    def get_objs(self):
        return(self._configuration_classes)

    def get(self, name):
        if name in self._config_items.keys():
            return(self._config_items[name])
        else:
            return(None)
        
    def factory_to_obj(self):
        for name, cls in self.get_objs().items():
            clsobj = cls(self.config,self.config.namespace(name))
            self._config_items[name] = clsobj
