import sys
sys.path.append('/Users/brendan/src/fancontrol/lib')
import json
import logging
from .factory import ConfigurationFactory

log = logging.getLogger(__name__)

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
                
            elif type(self._storage[name]) == dict:
                return_val = self.namespace(name)
            else:
                return_val = self._storage[name]
            
            if self.isnamespace(name):
                return_val = self._namespace[name]
            
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
        """Load configuration from the file."""
        try:
            with open(self._configfile, "r") as f:
                log.info(f"Loaded configuration from file: {self._configfile}")
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
        """Save configuration to the file."""
        modified = self._has_changed(self._storage)
        if modified:
            self._clean_obj(self._storage)
            with open(self._configfile, "w") as f:
                json.dump(self._storage, f)
            log.debug("Credentials saved.")
        else:
            log.debug("configuration not changed, not saved.")
            



class Configuration(ConfigurationBase):
    def __init__(self, DICT_OBJ, configfile="/config.json"):
        
        self._namespace = {}
        self._config_items = {}
        self._storage = DICT_OBJ
        
        log.debug(f"started Configuration with configfile {configfile}")
        super().__init__(configfile)
        
        if configfile:
            self.load_config()                
            self.config_to_factory(ConfigurationFactory())

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
    
    def config_to_factory(self, _configurationfactory):
        for name, clsobj in _configurationfactory.get_objs().items():
            self._config_items[name] = clsobj(self.namespace(name))      






