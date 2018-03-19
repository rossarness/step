import data as db
from customclasses import MyGrid
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

class AttributesBox(MyGrid):
    def __init__(self, **kwargs):
        super(AttributesBox, self).__init__(**kwargs)
        self.main_attributes = []

    def load_character(self):
        '''This method will load selected characters statistics'''
        self.main_attributes.extend((self.zw, self.inu, self.czj, self.um, self.kon, self.dh))
        self.char_name.disabled = True
        self.char_name.text = self.root_app.character
        children = self.children
        for child in children:
            if hasattr(child, 'focus'):
                child.bind(focus=self.save)
            if hasattr(child, 'children'):
                i = child.children
                for a in i:
                    if hasattr(a, 'focus'):
                        if hasattr(a, "name"):
                            if a.name is not "character_name":
                                new_value = db.get_attribute(self.root_app.character, a.name)
                                a.text = str(new_value)
                                a.bind(focus=self.save)
        for btn in self.main_attributes:
            new_value = db.get_attribute(self.root_app.character, btn.name)
            btn.text = str(new_value)

    def save(self, instance, value):
        '''This method saves changes to the attributes'''
        if not value:
            attr_value = instance.text
            attribute = instance.name
            db.save_attribute(self.root_app.character, attribute, attr_value)

class AttributesDropdown(DropDown):
    def __init__(self,**kwargs):
        super(AttributesDropdown, self).__init__(**kwargs)

    def on_select(self, data):
        parent_id = self.name
        if self.root.character is not None:
            db.save_attribute(self.root.character, parent_id, data)

class MainAttributeInput(Button):
    def __init__(self,**kwargs):
        super(MainAttributeInput, self).__init__(**kwargs)
        self.dropdown = AttributesDropdown()
        for index in range(10):
            text = str(index+1)
            btn = Button(text=text, size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self, 'text', x))

    def on_release(self):
        self.dropdown.root = self.parent.parent.root_app
        self.dropdown.name = self.name
        self.dropdown.open(self)