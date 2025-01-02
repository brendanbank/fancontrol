
import logging
log = logging.getLogger(__name__)


class Configuration(object):
    
    def __init__(self, storage):
        log.debug (f'started {self.__class__.__name__} ')
#         global object.storage
        object.__setattr__(self, "storage", storage)
        
    def _getitem(self, key):
        log.debug (f'{self.__class__.__name__}._getitem key: {key} ')
        return (self.storage.get(key))
        
    def _setitem (self,key, value):
        log.debug (f'{self.__class__.__name__}._setitem key: {key} value {value} ')
        self.storage.set(key,value)
        
    def _getattr(self, key):
        log.debug (f'{self.__class__.__name__}._getattr key: {key} ')
        return (self.storage.get(key))
    
    def _setattr (self,key, value):
        log.debug (f'{self.__class__.__name__}._setattr key: {key} value {value} ')
        self.storage.set(key,value)

    __getattr__ = _getattr
    __setattr__ = _setattr
    __getitem__ = _getitem
    __setitem__ = _setitem
    
    def get(self, key):
        log.debug (f'{self.__class__.__name__}.get key: {key} ')
        return (self._getattr(key))
        
    def __call__(self):
        return(self.storage())

    def namespace(self,name):
        return Configuration(self.storage.namespace(name))

    def save_config(self):
        return Configuration(self.storage.save_config())
    
    def load_config(self):
        return Configuration(self.storage.load_config())

    def __repr__(self):
        return(f'<{self.__class__.__name__} storage: {self.storage}>')

