from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.label import Label
from kivy.properties import BooleanProperty

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
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
        if is_selected:
            rv.item_selected(index)
        else:
            rv.item_unselected(index)
        rv.dispatch('on_items_changed')

class RV(RecycleView):
    def __init__(self, **kwargs):
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
        for item in reversed(items):
            self.data.pop(item)
        self.layout_manager.clear_selection()
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
        super(CharacterList, self).__init__(**kwargs)
        items = []
        self.data = items
        self.selected_item = None
        self.init_data()

    def item_selected(self, index):
        self.selected_item = index

    def item_unselected(self, index):
        pass

    def on_items_changed(self):
        if self.selected_item is None:
            self.del_btn.disabled = True
        else:
            self.del_btn.disabled = False

    def delete_items(self, item):
        self.data.pop(item)
        self.layout_manager.clear_selection()
        self.selected_item = None
        self.dispatch('on_items_changed')

    def init_data(self):
        self.data.append({'text': 'Character1'})
        self.data.append({'text': 'Character2'})