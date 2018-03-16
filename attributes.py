from customclasses import MyGrid

class AttributesBox(MyGrid):
    def __init__(self, **kwargs):
        super(AttributesBox, self).__init__(**kwargs)

    def load_character(self):
        '''This method will load selected characters statistics'''
        self.char_name.disabled = True
        self.char_name.text = self.root_app.character