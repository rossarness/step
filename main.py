import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.pagelayout import PageLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.properties import BooleanProperty

Builder.load_file('customclasses.kv')
Builder.load_file('equipment.kv')
Builder.load_file('attributes.kv')
kivy.require('1.10.0')

ITEMS=[{'text': str(x)} for x in range(10)]
ITEMS.append({'text': "Equipment Manual Test"})

class MainMenu(PageLayout):
    pass

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
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = ITEMS

class StepApp(App):

    def build(self):
        menu = MainMenu()
        return menu

if __name__ == '__main__':
    StepApp().run()
