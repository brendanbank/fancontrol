import sys
import json
import os
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
        config.factory = self
        
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

class NamespaceException(Exception):
    pass

class ConfigurationBase:
    def __init__(self, configfile="/config.json"):
        
        log.debug(f"started ConfigurationBase with configfile={configfile}")
        
        self._configfile = configfile
        self._storage['_modified'] = False
        
        def _get(name):
            if not name in self._storage.keys():
                log.debug(f'not name in _storage')
                self._storage[name] = return_val = None
                
            elif self.isnamespace(name):
                return_val = self.namespace(name)
            elif type(self._storage[name]) == dict:
                raise NamespaceException(f'"dict {name}" is not defined as a namespace!')
            else:
                return_val = self._storage[name]
                        
            log.debug(f'_get for {name} retured {return_val}')
            
            return return_val
        
        def _set(name, value):
            
            log.debug (f'_set called with {name} = {value}')

            if not name in self._storage.keys():
                self._storage[name] = None
            
            self._storage['_modified'] = True
            self._storage[name] = value
            
        self.__getattr__ = _get
        self.__setattr__ = _set

    def get (self,name):
        return (self.__getattr__(name))
    
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
            log.debug("uconfiguration saved.")
        else:
            log.debug("uconfiguration not changed, not saved.")
    
    def _get_config_by_name(self,name):
        return self._storage.get(name)
    
    def __repr__(self):
        return f'<{self.__class__.__name__} settings {self._storage}>'



class Configuration(ConfigurationBase):
    def __init__(self, DICT_OBJ={}, configfile="/config.json"):
        
        self._namespace = {}
        self._storage = DICT_OBJ
        self._itemfactory = list()
        
        log.debug(f"started Configuration with configfile {configfile}")
        super().__init__(configfile)
        
        if configfile:
            self.load_config()                

    @property
    def factory(self):
        return self._itemfactory[0]

    @factory.setter
    def factory(self, factory):
        if self._itemfactory:
            self._itemfactory[0] = factory
        else:
            self._itemfactory.append(factory)
            
    def isnamespace(self,namespace):
        return(getattr(self._namespace,namespace,None))

    def namespace(self,namespace):
        if not namespace in self._storage.keys():
            self._storage[namespace] = {}
            
        if not namespace in self._namespace.keys():
            log.debug(f'create namespace={namespace}')
            self._namespace[namespace] = Configuration(self._storage[namespace], configfile=None)

        return(self._namespace[namespace])
    
    # allows for item assignment like variabgel['test'] so the Configuration object behaves almost like a dict

    def __getitem__(self, key):
        return (self.__getattr__(key))
    def __setitem__(self, key, value):
        return (self.__setattr__(key,value))


if __name__ == "__main__":
    
    config = Configuration(configfile=None)
    print (config)
    config['a'] = 1
    print (config['a'])


    