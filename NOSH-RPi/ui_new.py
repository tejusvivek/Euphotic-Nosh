from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDIconButton, MDRectangleFlatButton

from screens import *
from widgets import *


class TestApp(MDApp):
    def build(self):
        builder = Builder.load_file('main.kv')
        return builder


if __name__ == '__main__':
    TestApp().run()
