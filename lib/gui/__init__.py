"""Defines the main GUI"""
import os
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from typing import List

from lib import params

class SelectionPopup(Popup):
    def __init__(self, name: str, data: List[str]):
        super(SelectionPopup, self).__init__()
        self.title: str = 'Select ' + name
        self.data: List[str] = data

    def get_data(self) -> List[str]:
        return self.data

class MainWidget(BoxLayout):
    def select_input(self) -> None:
        sp = SelectionPopup('input', ['#00 asdf', '#01 qwer'])
        print(sp.data)

    def select_output(self) -> None:
        pass

class FigaroApp(App):
    def build(self) -> None:
        self.title = 'Figaro'
        self.icon = os.path.join(params.BPATH, 'media', 'figaro.png')
        return MainWidget()

def start():
    """Displays the main GUI"""
    Window.clearcolor = (0, .08, .05, 1)
    # Builder.load_file(os.path.join(os.path.dirname(__file__), 'figaro.kv'))
    FigaroApp().run()