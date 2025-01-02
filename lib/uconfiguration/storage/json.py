import logging
log = logging.getLogger(__name__)
from uconfiguration.storage import StorageBase
import json
import os

class JsonStorage(StorageBase):

    def __init__(self,configfile="/config.json", *args, **kwargs):
        self._configfile = configfile
        super().__init__(*args, **kwargs)
        
        

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
                log.info(f"Loaded uconfiguration from file: {self._configfile} in '{os.getcwd()}'")
                config_obj = json.load(f)
                
        except Exception as e:
            log.warning(f'Error loading config file: {e}')
            config_obj = {}

        log.debug(f'loaded config = {config_obj}')
        for key in config_obj.keys():
            self._storage[key] = config_obj[key]

    def save_config(self):
        """Save uconfiguration to the file."""
        modified = self._has_changed(self.oldest_parent._storage)
        if modified:
            self._clean_obj(self.oldest_parent._storage)
            with open(self._configfile, "w") as f:
                json.dump(self.oldest_parent._storage, f)
            log.debug("uconfiguration saved.")
        else:
            log.debug("uconfiguration not changed, not saved.")


    def __repr__(self):
        return(f'<{self.__class__.__name__} configfile: {self._configfile} namespace: {self._namespace} storage:{self._storage}>')
