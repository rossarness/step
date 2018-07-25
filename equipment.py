import data as db
import os
from kivy.uix.popup import Popup
from kivy.utils import get_color_from_hex
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.graphics import InstructionGroup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import ObjectProperty # pylint: disable=E0611
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.dropdown import DropDown

class StatsLabel(Label):
    pass

class Equipment(RelativeLayout):
    '''This is base class for equipment screen'''
    def __init__(self, **kwargs):
        super(Equipment, self).__init__(**kwargs)

    def load_armor(self):
        '''This method is used for selecting armor for chosen character'''
        armor_items = [self.helm,
                       self.cape,
                       self.boots,
                       self.hand_1,
                       self.hand_2,
                       self.weapon_1,
                       self.weapon_2,
                       self.chest]
        for armor in armor_items:
            char = self.character.root_app.character
            char_id = db.get_character_id(char)
            item_id = db.load_character_item(char_id, armor.eq_id)
            if item_id:
                item = db.get_equipment_item(item_id)
                armor.source = item[0][2]
                armor.item_id = item_id
            else:
                armor.set_default_image()

class ImageButton(ButtonBehavior, Image):
    def on_press(self):
        pass

    def on_release(self):
        pass

class Add_item_Popup(Popup):
    '''This is base class for all eq popups'''
    def __init__(self, **kwargs):
        super(Add_item_Popup, self).__init__(**kwargs)
        self.add_btn.disabled = True
        self.new_item.bind(text=self.on_text)
    
    def on_add(self):
        pass

    def on_text(self, instance, value):
        if not value:
            self.add_btn.disabled = True
        else: 
            self.add_btn.disabled = False

class AddBackpackItemPopup(Add_item_Popup):
    def __init__(self, **kwargs):
        self.add_btn.bind(on_release=self.add_item)
        super(AddBackpackItemPopup, self).__init__(**kwargs)

    def add_item(self):
        self.item = self.new_item.text
        self.dispatch('on_add')
        self.dismiss()

class Tooltip(Label):
    pass

class Inventory_Btn(Button):
    pass

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Add_Inventory_Item_Template(Add_item_Popup):
    '''Popup used to add new inventory item'''
    def __init__(self, **kwargs):
        super(Add_Inventory_Item_Template, self).__init__(**kwargs)

    def add_item(self):
        self.item = self.new_item.text
        self.dismiss()

    def clear(self):
        if self.item_description.text == "Opis przedmiotu...":
            self.item_description.text = ""

    def load_image(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self.popup = Popup(title="Dodaj ikonę", content=content, size_hint=(0.9, 0.9))
        self.popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.chosen_image.source = stream.name
            self.image.text = stream.name
        self.dismiss_popup()

    def dismiss_popup(self):
        self.popup.dismiss()

class Add_Inventory_Item(Add_Inventory_Item_Template):
    pass

class Add_New_Weapon(Add_Inventory_Item_Template):
    def __init__(self, **kwargs):
        self.item_type = 'weapon'
        self.weapon = "Obrażenia"
        self.sub_type = None
        super(Add_New_Weapon, self).__init__(**kwargs)

class Add_New_Armor(Add_Inventory_Item_Template):
    def __init__(self, **kwargs):
        self.item_type = 'armor'
        super(Add_New_Armor, self).__init__(**kwargs)

class Add_New_Accessory(Add_Inventory_Item_Template):
    def __init__(self, **kwargs):
        self.item_type = 'accessory'
        self.sub_type = None
        super(Add_New_Accessory, self).__init__(**kwargs)

class Add_New_Inventory(Inventory_Btn):
    '''Button to add new inventory item'''
    def __init__(self, item_type, **kwargs):
        self.text = '+'
        self.inventory_type(item_type)
        super(Add_New_Inventory, self).__init__(**kwargs)

    def on_press(self):
        popup = self.type
        popup.add_btn.bind(on_release=lambda instance: self.menu.add_new_item(popup))
        popup.add_btn.bind(on_release=lambda instance: popup.dismiss())
        popup.open()

    def inventory_type(self, eq_id):
        print(eq_id)
        if eq_id == "weapon":
            self.type = Add_New_Weapon()
        elif eq_id == "armor":
            self.type = Add_New_Armor()
        elif eq_id == "accessory":
            self.type = Add_New_Accessory()
        else:
            self.type = Add_Inventory_Item()

class Inventory_Item(AnchorLayout):
    pass

class Inventory_Item_Btn(ImageButton):
    '''Item in the choose inventory menu'''
    def __init__(self, **kwargs):
        self.tooltip_displayed = False
        self.selected = False
        super(Inventory_Item_Btn, self).__init__(**kwargs)

    def on_press(self):
        pos = (self.popup.top * 0.79, self.popup.top * 0.87 )
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
    '''Popup with all inventory items'''
    def __init__(self, name, **kwargs):
        self.title = name
        super(EquipmentPopup, self).__init__(**kwargs)

    def choose_item(self):
        self.armor_btn.choose_item()

    def edit_item(self):
        self.armor_btn.edit_item()

class InfoPopup(Popup):
    '''Popup with information about equipment'''
    def __init__(self, name, text, **kwargs):
        self.title = name
        self.text = text
        super(InfoPopup, self).__init__(**kwargs)

class InfoButton(ImageButton):
    '''Button with information about equipment'''
    def __init__(self, **kwargs):
        super(InfoButton, self).__init__(**kwargs)

    def on_press(self):
        self.popup = InfoPopup(self.item_btn.text, self.desc)
        self.popup.open()

class EquipmentMenu(ImageButton):
    '''Button on Armor menu'''
    def __init__(self, **kwargs):
        self.selected_item = None
        self.items = 0
        super(EquipmentMenu, self).__init__(**kwargs)

    def on_press(self):
        self.popup = EquipmentPopup(self.name )
        self.popup.armor_btn = self
        eq_id = self.check_eq_id()
        item_type = map_item_type(eq_id)
        items = db.get_equipment_list(eq_id)
        for index in items:
            btn = Inventory_Item()
            self.items = self.items + 1
            btn.info_btn.desc = index[5]
            btn.item_btn.item_type = item_type
            btn.item_btn.item_id = index[0]
            btn.item_btn.text = index[1]
            if eq_id == "weapon":
                btn.info_btn.item_stat = index[4]
                btn.info_btn.sub_type = None
            elif eq_id == "cape":
                btn.info_btn.item_stat = None
                btn.info_btn.sub_type = None
            else:
                btn.info_btn.item_stat = index[6]
                btn.info_btn.sub_type = index[7]
            btn.item_btn.menu = self
            btn.item_btn.popup = self.popup
            btn.item_btn.source = index[2]
            self.popup.items.add_widget(btn)
            self.set_height()
        self.add_btn = Add_New_Inventory(item_type)
        self.add_btn.menu = self
        self.popup.items.add_widget(self.add_btn)
        self.popup.open()

    def add_new_item(self, item):
        '''Method used to add items to the equip'''
        btn = Inventory_Item()
        btn.item_btn.text = str(item.new_item.text)
        btn.item_btn.source = item.chosen_image.source
        eq_id = self.check_eq_id()
        item_type = map_item_type(eq_id)
        btn.item_btn.item_type = item_type
        btn.item_btn.item_id = db.add_equipment_item(item.new_item.text,
                                item.chosen_image.source, eq_id, item.item_stat.text,
                                item.item_description.text, item.sub_type.text)
        btn.item_btn.popup = self.popup
        btn.info_btn.item_stat = item.item_stat.text
        btn.info_btn.desc = item.item_description.text
        btn.info_btn.sub_type = item.sub_type.text
        self.items = self.items + 1
        btn.item_btn.menu = self
        self.popup.items.remove_widget(self.add_btn)
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
            self.popup.choose_btn.disabled = False
            self.popup.edit_btn.disabled = False
        elif self.selected_item is not item:
            item.selected = True
            self.add_canvas(item)
            self.selected_item = item
            self.popup.choose_btn.disabled = False
            self.popup.edit_btn.disabled = False
        else:
            self.popup.choose_btn.disabled = True
            self.popup.edit_btn.disabled = True
            self.remove_canvas(self.selected_item)
            self.selected_item = None

    def add_canvas(self, item):
        '''Adds selection canvas to button'''
        item.canvas.before.clear()
        rec_color = get_color_from_hex("#ccffcc")
        item.canvas.before.add(Color(rgba=rec_color))
        item.canvas.before.add(Rectangle(pos=item.pos,size=item.size))

    def set_height(self):
        '''Method will set height of the items list'''
        if self.items % 3 == 0:
            height_multiplier = (self.items / 3) + 1
            self.popup.items.height = 103 * height_multiplier

    def remove_canvas(self, item):
        '''Removes selection color from object'''
        item.canvas.before.clear()
        rec_color = get_color_from_hex("#808080")
        item.canvas.before.add(Color(rgba=rec_color))
        item.canvas.before.add(Rectangle(pos=item.pos,size=item.size))

    def choose_item(self):
        self.source = self.selected_item.source
        if self.equipment.character.root_app.character is not None:
                char = self.equipment.character.root_app.character
                eq_id = self.eq_id
                item_id = self.selected_item.item_id
                char_id = db.get_character_id(char)
                db.save_character_item(char_id, item_id, eq_id)
        self.popup.dismiss()

    def edit_item(self):
        item_type = self.selected_item.item_type
        if item_type == "weapon":
            popup = Add_New_Weapon()
        elif item_type == "accessory":
            popup = Add_New_Accessory()
        else:
            popup = Add_New_Armor()
        popup.chosen_image.source = self.selected_item.source
        popup.new_item.text = self.selected_item.text
        popup.add_btn.text = "Zapisz"
        popup.item_stat.text = str(self.selected_item.info_btn.item_stat)
        popup.item_description.text = self.selected_item.info_btn.desc
        if item_type == "armor":
            if self.selected_item.info_btn.sub_type != None:
                popup.sub_type.text = self.selected_item.info_btn.sub_type
        popup.add_btn.bind(on_release=lambda instance: self.save_item(popup))
        popup.open()

    def save_item(self, arg):
        print("DUPA" + arg.new_item.text)

    def check_eq_id(self):
        '''Method to select proper equipment for slot
        It's required because available equipment is the same for hand and
        weapon slots, so it uses same dictionary.
        But slots must be distinguished to determine what is equiped where'''
        if self.eq_id == "weapon_2":
            eq_id = "weapon"
        elif self.eq_id == "hand_2":
            eq_id = "hand"
        else:
            eq_id = self.eq_id
        return eq_id

    def set_default_image(self):
        '''Method used to revert button image to default'''
        self.source = self.default_src

class EquipmentButton(EquipmentMenu):
    pass

class WeaponButton(EquipmentButton):
    pass

class EquipmentAddButton(EquipmentUIButton):
    def __init__(self, **kwargs):
        super(EquipmentAddButton, self).__init__(**kwargs)

    def add_item(self, instance):
        new_item = self.popup.item
        self.item_list.data.append({"text": new_item})
        if self.equipment.character.root_app.character is not None:
            char = self.equipment.character.root_app.character
            db.add_backpack_item(char, new_item)

    def on_press(self):
        self.popup = AddBackpackItemPopup()
        self.popup.open()
        self.popup.register_event_type('on_add')
        self.popup.bind(on_add=self.add_item)

class EquipmentDeleteButton(EquipmentUIButton):
    def __init__(self, **kwargs):
        super(EquipmentDeleteButton, self).__init__(**kwargs)
        self.disabled = True

    def on_press(self):
        self.item_list.delete_items(self.item_list.selected_items)

def map_item_type(eq_id):
    '''Function used to map armor type to eq id'''
    if eq_id in ["weapon"]:
        return "weapon"
    elif eq_id in ["hand", "boots", "helm", "chest"]:
        return "armor"
    elif eq_id in ["cape"]:
        return "accessory"
    else:
        return "default"

class TypeDropdown(DropDown):
    def __init__(self,**kwargs):
        super(TypeDropdown, self).__init__(**kwargs)

class ArmorTypeInput(Button):
    def __init__(self,**kwargs):
        super(ArmorTypeInput, self).__init__(**kwargs)
        types = ["Lekki pancerz", "Średni Pancerz", "Ciężki Pancerz"]
        self.dropdown = TypeDropdown()
        for index in range(3):
            text = types[index]
            btn = Button(text=text, size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self, 'text', x))

    def on_release(self):
        self.dropdown.open(self)