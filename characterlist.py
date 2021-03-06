import data as db
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder

Builder.load_file("characters.kv")


class Characters(RelativeLayout):
    def __init__(self, **kwargs):
        super(Characters, self).__init__(**kwargs)

    def init_data(self):
        self.character_list.data.append({"text": "Character1"})

    def check_button(self):
        if self.character_list.selected_items:
            self.del_btn.disabled = False
        else:
            self.del_btn.disabled = True


class characterListButton(Button):
    pass


class AddCharacterButton(characterListButton):
    def __init__(self, **kwargs):
        super(AddCharacterButton, self).__init__(**kwargs)
        self.text = "Dodaj Postać"

    def add_item(self, instance):
        new_item = self.popup.item
        self.character_list.data.append({"text": new_item})
        db.add_character(new_item)

    def on_press(self):
        self.popup = AddCharacterPopup()
        self.popup.open()
        self.popup.register_event_type("on_add")
        self.popup.bind(on_add=self.add_item)


class RemoveCharacterButton(characterListButton):
    def __init__(self, **kwargs):
        super(RemoveCharacterButton, self).__init__(**kwargs)
        self.disabled = True
        self.text = "Usuń Postać"

    def on_press(self):
        self.character_list.delete_items(self.character_list.selected_item)


class AddCharacterPopup(Popup):
    def __init__(self, **kwargs):
        super(AddCharacterPopup, self).__init__(**kwargs)
        self.title = "Dodaj Postać"
        self.add_btn.disabled = True
        self.new_item.bind(text=self.on_text)

    def add_item(self):
        self.item = self.new_item.text
        try:
            db.check_duplicate_character(self.item)
            self.dispatch("on_add")
            self.dismiss()
        except NameError:
            self.new_item.foreground_color = [0.9, 0.2, 0.2, 1]
            self.char_exist.text = "Postać o podanym imieniu już istnieje!"

    def on_add(self):
        pass

    def on_text(self, instance, value):
        if not value:
            self.add_btn.disabled = True
        else:
            self.add_btn.disabled = False
