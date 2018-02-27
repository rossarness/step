from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder

Builder.load_file('characters.kv')

class Characters(RelativeLayout):
    def __init__(self, **kwargs):
        super(Characters, self).__init__(**kwargs)

    def init_data(self):
        self.character_list.data.append({'text': 'Character1'})

class characterListButton(Button):
    pass

class addCharacterButton(characterListButton):
    def __init__(self, **kwargs):
        super(addCharacterButton, self).__init__(**kwargs)

class removeCharacterButton(characterListButton):
    def __init__(self, **kwargs):
        super(removeCharacterButton, self).__init__(**kwargs)