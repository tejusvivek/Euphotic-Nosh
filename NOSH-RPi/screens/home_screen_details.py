from kivymd.uix.screen import MDScreen
from kivy.uix.gridlayout import GridLayout
from widgets import MyCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import *


class CookWidgetSocket(MDBoxLayout, FocusBehavior):
    pass


class ReheatWidgetSocket(MDBoxLayout):
    pass


class CleanWidgetSocket(MDBoxLayout):
    pass


class TasteWidgetSocket(MDBoxLayout):
    pass


class PowerWidgetSocket(MDBoxLayout):
    pass


class HomeScreen(MDScreen):

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        layout = GridLayout(cols=3)

        self.cook_widget = MyCard(header_text="Cook",
                                  image_source="resources/boiling.png")

        self.reheat_widget = MyCard(header_text="Reheat",
                                    image_source="resources/fried.png")

        self.clean_widget = MyCard(header_text="Clean",
                                   image_source="resources/spray.png")

        self.taste_widget = MyCard(header_text="Taste",
                                   image_source="resources/gears.png")

        self.power_widget = MyCard(header_text="Power",
                                   image_source="resources/power-off.png")

    def on_kv_post(self, base_widget):
        self.ids.cookwidgetsocket.add_widget(self.cook_widget)
        self.ids.reheatwidgetsocket.add_widget(self.reheat_widget)
        self.ids.cleanwidgetsocket.add_widget(self.clean_widget)
        self.ids.tastewidgetsocket.add_widget(self.taste_widget)
        self.ids.powerwidgetsocket.add_widget(self.power_widget)
