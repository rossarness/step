import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.pagelayout import PageLayout

Builder.load_file('customclasses.kv')
Builder.load_file('attributes.kv')
Builder.load_file('equipment.kv')
kivy.require('1.10.0')

class MainMenu(PageLayout):
    pass

class StepApp(App):

    def build(self):
        return MainMenu()

if __name__ == '__main__':
    StepApp().run()
