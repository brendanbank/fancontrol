
import logging
log = logging.getLogger(__name__)

class NamespaceException(Exception):
    pass

class ValueType(Exception):
    pass

class StorageBase (object):
    def __init__(self, DICT_OBJ={}, oldest_parent = None, namespace="main"):
        log.debug (f'started {self.__class__.__name__} ')
        self._storage = DICT_OBJ
        self._namespace = namespace
        self._namespaces = {}
        self.oldest_parent = oldest_parent
        if self.oldest_parent == None:
            self.oldest_parent = self
        
    def get (self,key):
        log.debug (f'Storage.get {self._storage} with key: {key}')

        if not key in self._storage.keys():
            log.debug(f'not name in _storage')
            self._storage[key] = return_val = None
            
        elif self.isnamespace(key):
            return_val = self.namespace(key)
        elif type(self._storage[key]) == dict:
            raise NamespaceException(f'"dict {key}" is not defined as a namespace!')
        else:
            return_val = self._storage[key]
                    
        log.debug(f'_get for {key} retured {return_val}')
        
        return return_val

    def set (self,key,value):
        self._storage[key] = value

        if not key in self._storage.keys():
            self._storage[key] = None
        
        self._storage['_modified'] = True
        
        if hasattr(value, '__dict__'):
            raise  ValueType(f'Cannot store an object, value is an instance of {type(value)}')

        self._storage[key] = value

        log.debug (f'Storage.set key: {key} value: {value}')

    def __call__(self):
        return(self._storage)

    def namespace(self,name):
        if not name in self._storage.keys():
            self._storage[name] = {}
            
        if not name in self._namespaces.keys():
            log.debug(f'create namespace={name}')
            self._namespaces[name] = StorageBase(DICT_OBJ=self._storage[name], oldest_parent=self.oldest_parent, namespace=name)

        return(self._namespaces[name])

    def commit(self):
        log.debug(f'commit')
        
    def isnamespace(self,namespace):
        return(getattr(self._namespace,namespace,None))

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
        for key in list(obj.keys()):
            if key == "_modified":
                del obj[key]
                continue
                
            if type(obj[key]) == dict:
                self._clean_obj(obj[key])
                
    def __repr__(self):
        return(f'<{self.__class__.__name__} namespace: {self._namespace} storage:{self._storage}>')

