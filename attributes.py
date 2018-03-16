import data as db
from customclasses import MyGrid

class AttributesBox(MyGrid):
    def __init__(self, **kwargs):
        super(AttributesBox, self).__init__(**kwargs)

    def load_character(self):
        '''This method will load selected characters statistics'''
        self.char_name.disabled = True
        self.char_name.text = self.root_app.character
        children = self.children
        for child in children:
            if hasattr(child, 'focus'):
                child.bind(focus=self.save)
            if hasattr(child, 'children'):
                i = child.children
                for a in i:
                    if a.disabled == True:
                        a.focus = False
                    elif hasattr(a, 'focus'):
                        if hasattr(a, "name"):
                            new_value = db.get_attribute(self.root_app.character, a.name)
                            a.text = str(new_value)
                        a.bind(focus=self.save)
    
    def save(self, instance, value):
        '''This method saves changes to the attributes'''
        if not value:
            attr_value = instance.text
            attribute = instance.name
            db.save_attribute(self.root_app.character, attribute, attr_value)