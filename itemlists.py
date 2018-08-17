from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.label import Label
from kivy.properties import BooleanProperty # pylint: disable=E0611
import data as db

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout): # pylint: disable=E0241
    pass

class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        rv.dispatch('on_items_changed')
        if is_selected:
            rv.item_selected(index)
        else:
            rv.item_unselected(index)
        rv.dispatch('on_items_changed')

class RV(RecycleView):
    def __init__(self, **kwargs):
        self.register_event_type('on_items_changed')
        super(RV, self).__init__(**kwargs)

class EquipmentList(RV):
    def __init__(self, **kwargs):
        self.register_event_type('on_items_changed')
        super(EquipmentList, self).__init__(**kwargs)
        items = []
        self.data = items
        self.selected_items = []

    def item_selected(self, index):
        self.selected_items.append(index)

    def item_unselected(self, index):
        try:
            self.selected_items.pop(index)
        except IndexError:
            pass

    def delete_items(self, items):
        deleted_items = []
        for item in reversed(items):
            try:
                deleted_items.append(self.data[item].get("text"))
                self.data.pop(item)
            except IndexError:
                try:
                    exception_id = item - 1
                    deleted_items.append(self.data[exception_id].get("text"))
                    self.data.pop(exception_id)
                except IndexError:
                    print("Item not found")
        self.layout_manager.clear_selection()
        if self.equipment.character.root_app.character is not None:
            character = self.equipment.character.root_app.character
            db.delete_backpack_item(character, deleted_items)
        self.selected_items = []
        self.dispatch('on_items_changed')

    def on_items_changed(self):
        if self.selected_items == []:
            self.del_btn.disabled = True
        else:
            self.del_btn.disabled = False

class CharacterList(RV):
    def __init__(self, **kwargs):
        self.register_event_type('on_items_changed')
        self.register_event_type('on_character_changed')
        super(CharacterList, self).__init__(**kwargs)
        items = []
        self.data = items
        self.selected_item = None
        self.init_data()

    def item_selected(self, index):
        self.selected_item = index
        self.character.root_app.character = self.data[index].get("text")
        self.dispatch('on_character_changed')

    def item_unselected(self, index):
        pass

    def on_items_changed(self):
        if self.selected_item is None:
            self.del_btn.disabled = True
        else:
            self.del_btn.disabled = False

    def on_character_changed(self):
        self.character.equipment.item_list.data = []
        items = db.get_backpack_list(self.character.root_app.character)
        if items is not []:
            for item in items:
                self.character.equipment.item_list.data.append({'text': item})
        self.character.attributes.load_character()
        self.character.equipment.load_armor()

    def delete_items(self, item):
        self.data.pop(item)
        db.delete_character(self.character.root_app.character)
        self.character.root_app.character = None
        self.layout_manager.clear_selection()
        self.selected_item = None
        self.dispatch('on_items_changed')

    def init_data(self):
        chars_from_db = db.get_character_list()
        for char in chars_from_db:
            self.data.append({"text": char})