from kivymd.uix.screen import MDScreen, Screen
from kivy.uix.gridlayout import GridLayout

from widgets import MyCardWidget

from kivy.uix.button import ButtonBehavior
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.boxlayout import MDBoxLayout


class CookWidgetSocket(MDBoxLayout):
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

        self.cook_widget = MyCardWidget(header_text="Cook",
                                        image_path="resources/boiling.png")

        self.reheat_widget = MyCardWidget(header_text="Reheat",
                                          image_path="resources/fried.png")

        self.clean_widget = MyCardWidget(header_text="Clean",
                                         image_path="resources/spray.png")

        self.taste_widget = MyCardWidget(header_text="Taste",
                                         image_path="resources/gears.png")

        self.power_widget = MyCardWidget(header_text="Power",
                                         image_path="resources/power-off.png")

    def on_kv_post(self, base_widget):

        self.ids.cookwidgetsocket.add_widget(self.cook_widget)
        self.ids.reheatwidgetsocket.add_widget(self.reheat_widget)
        self.ids.cleanwidgetsocket.add_widget(self.clean_widget)
        self.ids.tastewidgetsocket.add_widget(self.taste_widget)
        self.ids.powerwidgetsocket.add_widget(self.power_widget)

