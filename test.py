

class Base:
    startup = ['none']

class A(Base):
    startup = [ 'a' ]
    
    def __init__(self):
        pass
    
    
class B(Base):
    startup = [ 'b' ]

    def __init__(self):
        pass

class C(Base):

    def __init__(self):
        pass


l = [ A(), B(), C()]

for i in l:
    print (i.startup)
