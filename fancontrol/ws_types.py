import logging

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
class WebSocketHandler(logging.Handler):

    def __init__(self, ws_logging_list, *args, **kwargs):
        self.ws_logging_list = ws_logging_list
        super().__init__(*args, **kwargs)
        
    def emit(self, record):
        self.ws_logging_list.append(record.__dict__)
