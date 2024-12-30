from test import FormBase, Text, Number

class MyForm(FormBase):

    text = Text(validation="yes")
    number = Number(css="No")
    
test = MyForm()

test.newInstance()

# test.a = "bla"
