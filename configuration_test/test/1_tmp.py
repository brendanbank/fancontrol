import sys
sys.path.append('/Users/brendan/src/fancontrol/configuration_test')

from items import BaseItem

class prio_2(BaseItem):
    _priority = 2
    
    """ wifi uconfiguration class """
    config_attribute = True
    item_name = 'prio_2'
    config_description = 'prio_2'
    startup_methods = [ 'test_method' ]


    def test_method(sefl):
        print ("test_method called")
