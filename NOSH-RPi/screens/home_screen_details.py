from kivymd.uix.screen import MDScreen
from kivy.uix.gridlayout import GridLayout

from widgets import *


class HomeScreen(MDScreen):

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        layout = GridLayout(rows=2, cols=3)
        self.add_widget(layout)

        cook_widget = MyCardWidget(header_text="Cook",
                                   content_text="Cooking Page",
                                   image_path="resources/microwave-oven.png")

        reheat_widget = MyCardWidget(header_text="Reheat",
                                   content_text="Reheat Page",
                                   image_path="resources/Reheat.png")

        clean_widget = MyCardWidget(header_text="Clean",
                                   content_text="Cleaning Page",
                                   image_path="resources/Clean.png")

        taste_widget = MyCardWidget(header_text="Taste",
                                     content_text="Taste Page",
                                     image_path="resources/Taste Configuration.png")

        power_widget = MyCardWidget(header_text="Power",
                                     content_text="Power Page",
                                     image_path="resources/Power Off.png")

        layout.add_widget(cook_widget)
        layout.add_widget(reheat_widget)
        layout.add_widget(clean_widget)
        layout.add_widget(taste_widget)
        layout.add_widget(power_widget)


