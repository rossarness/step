import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.pagelayout import PageLayout

kivy.require('1.10.0')

class MainMenu(PageLayout):
    pass

class StepApp(App):

    def build(self):
        return MainMenu()

if __name__ == '__main__':
    StepApp().run()
