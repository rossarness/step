import kivy
import characterlist
import itemlists
import equipment
import attributes
import customclasses
import skills
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.pagelayout import PageLayout
from kivy.config import Config
from kivy.core.window import Window

Builder.load_file('customclasses.kv')
Builder.load_file('equipment.kv')
Builder.load_file('attributes.kv')
Builder.load_file('skills.kv')
kivy.require('1.10.0')

Config.set('graphics', 'width', '1480')
Config.set('graphics', 'height', '720')
Config.set('graphics', 'resizable', '0' )
Window.size = (1480, 720)

class MainMenu(PageLayout):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.character = None

class CompanionApp(App):
    title = 'Dark Futura Companion App v. 0.1.0'

    def build(self):
        menu = MainMenu()
        return menu

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == '__main__':
    CompanionApp().run()