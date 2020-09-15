from kivy.config import Config

Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'resizable', '0')

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFloatingActionButtonSpeedDial, MDIconButton, MDRectangleFlatButton
from kivymd.uix.behaviors import *
from kivymd.uix.button import ButtonBehavior
from kivy.core.window import Window

from screens import *
from widgets import *


class NewApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)


    def build(self):
        builder = Builder.load_file('main.kv')
        sm = ScreenManager()
        return builder

    def on_start(self):
        self.screenmanager = self.root
        print(self.screenmanager.screens)

        for screens in self.screenmanager.screens:
            print(screens)

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keycode == 30:
            print("focus on cook screen")


        # print('The key', keycode, 'have been pressed')
        # print(' - text is %r' % text)
        # print(' - modifiers are %r' % modifiers)

        # if keyboard in (1001, 27):
        #     if self.manager_open:
        #         self.file_manager.back()
        return True


if __name__ == '__main__':
    NewApp().run()
