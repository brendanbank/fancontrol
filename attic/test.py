
import types
import sys

class FormItemBase:
    def __init__(self, *args, **kwargs):
        self._kwargs = kwargs
        self._args = args
        log.debug (f'{__class__.__name__}/{self.__class__.__name__} created in {__name__} with *_args = {args} **kwargs = {kwargs}')
        

class Text(FormItemBase):
    """ Text """
    def __init__(self, *args, **kwargs):
        log.debug (f'{__class__.__name__}/{self.__class__.__name__} created in {__name__} with *_args = {args} **kwargs = {kwargs}')
        super().__init__(*args, **kwargs)

    
class Number(FormItemBase):
    """ Text """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        log.debug (f'{__class__.__name__}/{self.__class__.__name__} created in {__name__} with *_args = {args} **kwargs = {kwargs}')

class FormBase(object):
    def __init__(self, css=""):
        self.css = css
        self.form_items = {}
        self._order = list()
        self._class_args = list()
        self._cls = None
        self._fill_self()
        self._create_empty_class()
        
        
    def _fill_self(self):
        for cls_attribute in dir(self):
            try:
                obj = getattr(self.__class__, cls_attribute)
            except:
                continue

            if issubclass(obj.__class__, FormItemBase):
                self._order.append(cls_attribute)
                clsobj = getattr(self, cls_attribute)
                clsobj.name = cls_attribute
                self.form_items[cls_attribute] = clsobj
                
                self._class_args.append(
                                    {'_name': cls_attribute,
                                     '_args': clsobj._args ,
                                     '_kwargs': clsobj._kwargs,
                                     '_cls': obj.__class__
                                })

    def _create_empty_class(self):
        name = 'Dynamnic' + self.__class__.__name__
        
        def clsexec(ns):
            attrs = []
            ns['type'] = name
            ns['attrs'] = attrs
            
        self._cls = types.new_class(name, bases=(FormBase,), exec_body=clsexec)


    def newInstance(self):
        new_formbase = FormBase()
        log.debug (self.__class__.__name__)
        
        clsobj = self._cls()
        
        for form_item in self._class_args:
            print (form_item)
            setattr(clsobj, form_item['_name'], form_item['_cls'](form_item['_args'],form_item['_kwargs']) )
            
        return(clsobj)
        

if __name__ == "__main__":
    import sys
    sys.path.append('/Users/brendan/src/fancontrol/lib')
    import os
    import logging

    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__)

    class MyForm(FormBase):

        text = Text(validation="yes", bla="now")
        number = Number(css="No")
        
    test = MyForm()

    clsobj = test.newInstance()
    
    print (clsobj.text)
    
    log.debug (clsobj)
