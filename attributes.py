import data as db
from customclasses import MyGrid
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox

class AttributesBox(MyGrid):
    def __init__(self, **kwargs):
        super(AttributesBox, self).__init__(**kwargs)
        self.main_attributes = []

    def load_character(self):
        '''This method will load selected characters statistics'''
        self.main_attributes.extend((self.zw,
                                     self.inu,
                                     self.czj,
                                     self.um,
                                     self.kon,
                                     self.dh))
        self.char_name.disabled = True
        self.char_name.text = self.root_app.character
        children = self.children
        exhaustion = [self.tired_0, self.tired_1, self.tired_2, self.tired_3]
        for tired in exhaustion:
            tired.active = False
            tired.bind(on_exhaustion_change=self.save)
        tired = db.get_attribute(self.root_app.character, 'tired')
        if tired == 1:
            self.tired_1.active = True
        elif tired == 2:
            self.tired_2.active = True
        elif tired == 3:
            self.tired_3.active = True
        else:
            self.tired_0.active = True
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
        if self.dh.text is not ' ' and self.dh.text is not None:
            self.dh.check_health()
        else:
            self.kon.check_health()

    def save(self, instance, value):
        '''This method saves changes to the attributes'''
        if not value:
            if hasattr(instance, 'text'):
                attr_value = instance.text
                attribute = instance.name
                db.save_attribute(self.root_app.character, attribute, attr_value)
        if hasattr(instance, 'active') and instance.active == True:
                attribute = 'tired'
                db.save_attribute(self.root_app.character, attribute, value)

    def update_health(self, hp_value):
        '''This method updates the total value of health'''
        total_health = []
        total_health.extend((self.zd_total,
                            self.lr_total,
                            self.sr_total,
                            self.cr_total,
                            self.kr_total,
                            self.um_total))
        for hp_item in total_health:
            hp_item.text = str(hp_value)

class AttributesDropdown(DropDown):
    def __init__(self,**kwargs):
        super(AttributesDropdown, self).__init__(**kwargs)

    def on_select(self, data):
        parent_id = self.name
        if self.root.character is not None:
            db.save_attribute(self.root.character, parent_id, data)

    def on_dismiss(self):
        self.hp_parent.check_health()

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
        self.dropdown.hp_parent = self
        self.dropdown.name = self.name
        self.dropdown.open(self)

    def check_health(self):
        if self.name == "kon" or "dh":
            kon = self.parent.parent.kon.text
            dh = self.parent.parent.dh.text
            if kon is not None and dh is not None and kon is not ' ' and dh is not ' ':
                if kon > dh:
                    total_hp = 10 + int(kon)
                else:
                    total_hp = 10 + int(dh)
            elif self.text is not None and self.text is not ' ':
                total_hp = int(self.text) + 10
            else:
                total_hp = 0
            self.parent.parent.update_health(total_hp)

class Total_Health(Label):
    pass

class Tired(CheckBox):
    '''Radio button to keep tired level of the character'''
    def __init__(self, **kwargs):
        super(Tired, self).__init__(**kwargs)
        self.register_event_type("on_exhaustion_change")

    def on_state(self, instance, value):
        if value == 'down':
            self.active = True
            self.dispatch("on_exhaustion_change", self.value)
        else:
            self.active = False
    
    def on_exhaustion_change(self, value):
        pass