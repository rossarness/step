import data as db
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.graphics import InstructionGroup


class Add_Equipment_Popup(Popup):
    '''This is base class for all eq popups'''
    def __init__(self, **kwargs):
        super(Add_Equipment_Popup, self).__init__(**kwargs)
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

class AddEquipmentPopup(Add_Equipment_Popup):
    pass

class Tooltip(Label):
    pass

class Inventory_Btn(Button):
    pass

class Add_Inventory_Item(Add_Equipment_Popup):
    pass

class Add_New_Inventory(Inventory_Btn):
    def __init__(self, **kwargs):
        self.text = '+'
        super(Add_New_Inventory, self).__init__(**kwargs)

    def on_press(self):
        popup = Add_Inventory_Item()
        popup.open()
        popup.register_event_type('on_add')
        popup.bind(on_add=lambda popup: self.add_item(popup.new_item.text))

    def add_item(self, item):
        self.menu.add_new_item(item)

class Inventory_Item(Inventory_Btn):
    def __init__(self, **kwargs):
        self.tooltip_displayed = False
        self.selected = False
        super(Inventory_Item, self).__init__(**kwargs)

    def on_press(self):
        pos = self.pos
        self.tooltip = Tooltip(text=self.text)
        self.tooltip.pos = (pos)
        self.display_tooltip()

    def on_release(self):
        if self.tooltip_displayed:
            self.close_tooltip()
            self.tooltip_displayed = False
        self.menu.select_item(self)

    def close_tooltip(self, *args):
        Window.remove_widget(self.tooltip)

    def display_tooltip(self, *args):
        self.tooltip_displayed = True
        Window.add_widget(self.tooltip)

class EquipmentUIButton(Button):
    pass

class EquipmentPopup(Popup):
    def __init__(self, name, **kwargs):
        self.title = name
        super(EquipmentPopup, self).__init__(**kwargs)

class EquipmentMenu(Button):
    def __init__(self, **kwargs):
        self.selected_item = None
        self.items = 0
        super(EquipmentMenu, self).__init__(**kwargs)

    def on_press(self):
        self.popup = EquipmentPopup(self.name )
        for index in range(10):
            btn = Inventory_Item()
            self.items = self.items + 1
            btn.text = str(index)
            btn.menu = self
            self.popup.items.add_widget(btn)
            self.set_height()
        self.add_btn = Add_New_Inventory()
        self.add_btn.menu = self
        self.popup.items.add_widget(self.add_btn)
        self.popup.open()

    def add_new_item(self, new_item):
        '''Method used to add items to the equip'''
        self.popup.items.remove_widget(self.add_btn)
        btn = Inventory_Item()
        btn.text = str(new_item)
        self.items = self.items + 1
        btn.menu = self
        self.popup.items.add_widget(btn)
        self.popup.items.add_widget(self.add_btn)
        self.set_height()

    def select_item(self, item, *args):
        '''Method used to mark item as selected'''
        if self.selected_item is not item and self.selected_item is not None:
            self.selected_item.selected = False
            self.remove_canvas(self.selected_item)
            item.selected = True
            self.add_canvas(item)
            self.selected_item = item
        elif self.selected_item is not item:
            item.selected = True
            self.add_canvas(item)
            self.selected_item = item
        else:
            pass

    def add_canvas(self, item):
        '''Adds selection canvas to button'''
        item.background_color = (0, 0.6, 0, 1)

    def set_height(self):
        '''Method will set height of the items list'''
        if self.items % 5 == 0:
            height_multiplier = (self.items / 5) + 1
            self.popup.items.height = 64 * height_multiplier

    def remove_canvas(self, item):
        '''Removes selection color from object'''
        item.background_color = (1, 1, 1, 1)

class EquipmentButton(EquipmentMenu):
    pass

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