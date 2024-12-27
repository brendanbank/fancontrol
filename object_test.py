class PropClass(object):
    def __getattribute__(self, attr):
        val = super().__getattribute__(attr)
        if callable(val):
            print (f"callable {val}")
            return val
        else:
            print (f"not callable {val}")
            return val
        

        
        
class Foo(PropClass):
    def __init__(self):
        pass

a = Foo()
a.b = 1

print (a.b)

print (dir (a))