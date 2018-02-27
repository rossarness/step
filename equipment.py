from kivy.uix.popup import Popup
from kivy.uix.button import Button

class EquipmentPopup(Popup):
    def __init__(self, name, **kwargs):
        super(EquipmentPopup, self).__init__(**kwargs)

class EquipmentMenu(Button):
    def __init__(self, **kwargs):
        self.selected = None
        super(EquipmentMenu, self).__init__(**kwargs)

    def on_press(self):
        self.popup = EquipmentPopup(self.name, title="Test")
        self.popup.open()

class EquipmentButton(EquipmentMenu):
    pass

class EquipmentUIButton(Button):
    pass

class AddEquipmentPopup(Popup):
    def __init__(self, **kwargs):
        super(AddEquipmentPopup, self).__init__(**kwargs)

    def add_item(self):
        self.item = self.new_item.text
        self.dismiss()

class EquipmentAddButton(EquipmentUIButton):
    def __init__(self, **kwargs):
        super(EquipmentAddButton, self).__init__(**kwargs)

    def add_item(self, instance):
        new_item = self.popup.item
        self.item_list.data.append({"text": new_item})

    def on_press(self):
        self.popup = AddEquipmentPopup()
        self.popup.open()
        self.popup.bind(on_dismiss=self.add_item)

class EquipmentDeleteButton(EquipmentUIButton):
    def __init__(self, **kwargs):
        super(EquipmentDeleteButton, self).__init__(**kwargs)

    def on_press(self):
        if self.item_list.selected_items == []:
            print("wowowoow")
        else:
            self.item_list.delete_items(self.item_list.selected_items)