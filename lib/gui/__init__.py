"""Defines the main GUI"""
import os
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

from lib import params

class MainLayout(BoxLayout):
    pass

class FigaroApp(App):
    def build(self) -> None:
        self.title = 'Figaro'
        self.icon = os.path.join(params.BPATH, 'media', 'figaro.png')
        return MainLayout()

def start():
    """Displays the main GUI"""
    Window.clearcolor = (0, .08, .05, 1)
    Builder.load_file(os.path.join(os.path.dirname(__file__), 'figaro.kv'))
    FigaroApp().run()