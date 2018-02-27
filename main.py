import kivy
import characterlist
import itemlists
import equipment
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.pagelayout import PageLayout


Builder.load_file('customclasses.kv')
Builder.load_file('equipment.kv')
Builder.load_file('attributes.kv')
Builder.load_file('characters.kv')
kivy.require('1.10.0')

class MainMenu(PageLayout):
    pass

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
