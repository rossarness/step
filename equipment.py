import data as db
from kivy.uix.popup import Popup
from kivy.uix.button import Button

class Inventory_Btn(Button):
    pass

class Add_New_Inventory(Inventory_Btn):
    def __init__(self, **kwargs):
        self.text = '+'
        super(Add_New_Inventory, self).__init__(**kwargs)

class Inventory_Item(Inventory_Btn):
    pass

class EquipmentUIButton(Button):
    pass

class EquipmentPopup(Popup):
    def __init__(self, name, **kwargs):
        self.title = name
        super(EquipmentPopup, self).__init__(**kwargs)

class EquipmentMenu(Button):
    def __init__(self, **kwargs):
        super(EquipmentMenu, self).__init__(**kwargs)

    def on_press(self):
        self.popup = EquipmentPopup(self.name )
        for index in range(10):
            btn = Inventory_Btn()
            btn.text = str(index)
            btn.bind(on_press=self.choose_item)
            self.popup.items.add_widget(btn)
        add_btn = Add_New_Inventory()
        self.popup.items.add_widget(add_btn)
        self.popup.open()

    def choose_item(self, btn):
        '''Method used to select item to equip'''
        print(self.name)
        print(btn.text)

class EquipmentButton(EquipmentMenu):
    pass

class AddEquipmentPopup(Popup):
    def __init__(self, **kwargs):
        super(AddEquipmentPopup, self).__init__(**kwargs)
        self.add_btn.disabled = True
        self.new_item.bind(text=self.on_text)

    def add_item(self):
        self.item = self.new_item.text
        self.dispatch('on_add')
        self.dismiss()
    
    def on_add(self):
        pass

    def on_text(self, instance, value):
        if not value:
            self.add_btn.disabled = True
        else: 
            self.add_btn.disabled = False

class EquipmentAddButton(EquipmentUIButton):
    def __init__(self, **kwargs):
        super(EquipmentAddButton, self).__init__(**kwargs)

    def add_item(self, instance):
        new_item = self.popup.item
        self.item_list.data.append({"text": new_item})
        if self.equipment.character.root_app.character is not None:
            char = self.equipment.character.root_app.character
            db.add_equipment(char, new_item)

    def on_press(self):
        self.popup = AddEquipmentPopup()
        self.popup.open()
        self.popup.register_event_type('on_add')
        self.popup.bind(on_add=self.add_item)

class EquipmentDeleteButton(EquipmentUIButton):
    def __init__(self, **kwargs):
        super(EquipmentDeleteButton, self).__init__(**kwargs)
        self.disabled = True

    def on_press(self):
        self.item_list.delete_items(self.item_list.selected_items)