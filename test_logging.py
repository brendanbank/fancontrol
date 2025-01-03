import sys
sys.path.append('/Users/brendan/src/fancontrol/lib')
import logging
import time

class BoundedList:
    def __init__(self, max_size):
        """
        Initialize the BoundedList with a maximum size.

        :param max_size: Maximum number of entries allowed in the list.
        """
        if max_size <= 0:
            raise ValueError("max_size must be greater than 0")
        self.max_size = max_size
        self._list = []

    def append(self, item):
        """
        Add an item to the list. If the list exceeds the maximum size, remove the oldest entry.

        :param item: Item to add to the list.
        """
        self._list.append(item)
        if len(self._list) > self.max_size:
            self._list.pop(0)  # Remove the oldest entry

    def __repr__(self):
        """Return a string representation of the list."""
        return repr(self._list)

    def __len__(self):
        """Return the number of items in the list."""
        return len(self._list)

    def __getitem__(self, index):
        """Allow indexing into the list."""
        return self._list[index]

    def __setitem__(self, index, value):
        """Allow setting items in the list."""
        self._list[index] = value

    def __delitem__(self, index):
        """Allow deleting items from the list."""
        del self._list[index]

    def __iter__(self):
        """Allow iteration over the list."""
        return iter(self._list)

    def clear(self):
        """Clear all items in the list."""
        self._list.clear()

    def extend(self, iterable):
        """
        Extend the list with items from an iterable.
        Automatically manages size if the resulting list exceeds max_size.

        :param iterable: An iterable of items to extend the list with.
        """
        for item in iterable:
            self.append(item)
            

# class Listandler(logging.Handler):
#     def __init__(self,logging_list, *args, **kwargs):
#         
#         self.logging_list = logging_list
#         super().__init__(*args, **kwargs)
#         
#     def emit(self, record):
#         self.logging_list.append(record.__dict__)
# 
# # Create logger
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# 
# # Create console handler and set level to debug
# stream_handler = logging.StreamHandler()
# stream_handler.setLevel(logging.DEBUG)
# 
# 
# # Create a formatter
# formatter = logging.Formatter("Stream: %(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s")
# 
# # Default Logger
# 
# stream_handler.setFormatter(formatter)

# formatter = logging.Formatter("Stream: %(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s")
#

logging_list = BoundedList(3)

class WebSocketHandler(logging.Handler):

    def __init__(self, ws_logging_list, *args, **kwargs):
        self.ws_logging_list = ws_logging_list
        super().__init__(*args, **kwargs)
        
    def emit(self, record):
        self.ws_logging_list.append(record.__dict__)
# 
# class ConsoleHandler(logging.Handler):
#     def emit(self, record):
#         print("ConsoleHandler %(name)s - %(levelname)s - %(message)s" % record.__dict__)


logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
# for handler in logging.getLogger().handlers:
#     handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s:%(message)s"))

logging.getLogger().addHandler(WebSocketHandler(logging_list))

logging.info("hello upy")
logging.getLogger("child").info("hello 2")
logging.getLogger("child").debug("hello 2")

logging.getLogger().setLevel(logging.DEBUG)

logging.info("hello upy")
logging.getLogger("child").info("hello 2")
logging.getLogger("child").debug("hello 2")

log = logging.getLogger("child")

log.debug("Test")

print (logging_list)

# log = logging.getLogger("a")
# log.setLevel(logging.DEBUG)
# log.addHandler(WebHandler())
# log.addHandler(ConsoleHandler())
# log.debug("test")
# 
# log.setLevel(logging.INFO)
# logging.basicConfig(level=logging.DEBUG)
# log = logging.getLogger(__name__)
# 
# log.debug("test")
# log.info("test")
# 
# print(logging._loggers)



# logging.basicConfig(level=logging.DEBUG)
# log = logging.getLogger(__name__)
# log.addHandler(WebHandler())

# log = logging.getLogger(__name__)
# 
# log.addHandler(MyHandler())
# 
# log.setLevel(logging.DEBUG)
# 
# log.debug("Test")
# log.debug("Test")
# 
# log2 = logging.getLogger(__name__)
