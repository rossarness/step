import kivy
import characterlist
import itemlists
import equipment
import attributes
import customclasses
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.pagelayout import PageLayout


Builder.load_file('customclasses.kv')
Builder.load_file('equipment.kv')
Builder.load_file('attributes.kv')
kivy.require('1.10.0')

class MainMenu(PageLayout):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.character = None

class StepApp(App):
    title = 'Step'

    def build(self):
        menu = MainMenu()
        return menu

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    StepApp().run()
