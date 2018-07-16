from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty # pylint: disable=E0611

class MyGrid(GridLayout):
    pass

class Step_Label(Label):
    pass

class Step_Input(TextInput):
    pass

class Step_Input_Focus(Step_Input):
    def __init__(self, **kwargs):
        super(Step_Input_Focus, self).__init__(**kwargs)

class ScrollableLabel(ScrollView):
    text = StringProperty('')