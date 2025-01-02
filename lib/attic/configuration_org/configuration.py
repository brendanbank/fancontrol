import sys
import json
import os
import logging

log = logging.getLogger(__name__)

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
    
    def __init__(self, item_directory = None):
        self._configuration_classes = dict()
        self.item_directory = item_directory
        self._register()

    def _register(self):
        if self.item_directory:
            for fiel in os.listdir(self.item_directory):                               
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
            return(self._configuration_classes.get(name))
        else:
            return(None)

class NamespaceException(Exception):
    pass

class ConfigurationBase:
    def __init__(self, configfile="/config.json"):
        
        log.debug(f"started ConfigurationBase with configfile={configfile}")
        
        self._configfile = configfile
        self._storage['_modified'] = False
        
        def _get(name):
                
            if not name in self._storage.keys():
                self._storage[name] = return_val = None
                
            elif self.isnamespace(name):
                return_val = self.namespace(name)
            else:
                return_val = self._storage[name]
                        
            log.debug(f'_get for {name} retured {return_val}')
            
            return return_val
        
        def _set(name, value):
            
            log.debug (f'_set called with {name} = {value}')

            if not name in self._storage.keys():
                self._storage[name] = None
            if type(self._storage[name]) == dict:
                raise NamespaceException(f'"{name}" is defined as a namespace!')
            
            self._storage['_modified'] = True
            self._storage[name] = value
            
        self.__getattr__ = _get
        self.__setattr__ = _set

    @property
    def __DO_NOT_REMOVE(self):
        pass
    
    def from_json(self, json_str):
        config_dict = json.loads(json_str)
        for key in config_dict.keys():
            self._storage[key] = config_dict[key]

    @property
    def json(self):
        return json.dumps(self._storage)

    def load_config(self):
        """Load uconfiguration from the file."""
        try:
            with open(self._configfile, "r") as f:
                log.info(f"Loaded uconfiguration from file: {self._configfile}")
                config_obj = json.load(f)
                
        except Exception as e:
            log.warning(f'Error loading config file: {e}')
            config_obj = {}

        log.debug(f'loaded config = {config_obj}')
        for key in config_obj.keys():
            self._storage[key] = config_obj[key]

    def _has_changed(self, obj):
        modified = False
        for key in obj.keys():
            if key == "_modified" and obj["_modified"] == True:
                modified =  True
            if type(obj[key]) == dict:
                if (self._has_changed(obj[key])):
                    modified = True
        
        return (modified)
    
    def _clean_obj(self,obj):
        for key in obj.keys():
            if key == "_modified":
                del obj[key]
                continue
                
            if type(obj[key]) == dict:
                self._clean_obj(obj[key])
    
    def save_config(self):
        """Save uconfiguration to the file."""
        modified = self._has_changed(self._storage)
        if modified:
            self._clean_obj(self._storage)
            with open(self._configfile, "w") as f:
                json.dump(self._storage, f)
            log.debug("Credentials saved.")
        else:
            log.debug("uconfiguration not changed, not saved.")
            



class Configuration(ConfigurationBase):
    def __init__(self, DICT_OBJ, configfile="/config.json"):
        
        self._namespace = {}
        self._config_items = {}
        self._storage = DICT_OBJ
        
        log.debug(f"started Configuration with configfile {configfile}")
        super().__init__(configfile)
        
        if configfile:
            self.load_config()                
            self.config_to_factory()

    def get_config_item(self,item):
        return(self._config_items[item])
    
    def isnamespace(self,namespace):
        return(getattr(self._namespace,namespace,None))

    def namespace(self,namespace):
        if not namespace in self._storage.keys():
            self._storage[namespace] = {}
            
        if not namespace in self._namespace.keys():
            log.debug(f'create namespace={namespace}')
            self._namespace[namespace] = Configuration(self._storage[namespace], configfile=None)

        return(self._namespace[namespace])
    
    def config_to_factory(self, _configurationfactory=ItemFactory()):
        for name, clsobj in _configurationfactory.get_objs().items():
            self._config_items[name] = clsobj(self,self.namespace(name))      






