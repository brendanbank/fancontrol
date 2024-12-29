import sys
from configuration import ItemBase

class prio_2(ItemBase):
    _priority = 2
    
    """ wifi configuration class """
    config_attribute = True
    item_name = 'prio_2'
    config_description = 'prio_2'
    startup_methods = [ 'test_method' ]


    def test_method(sefl):
        print ("test_method called")
