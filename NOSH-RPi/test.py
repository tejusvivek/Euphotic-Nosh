from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation

from kivymd.app import MDApp
from kivymd.uix.expansionpanel import MDExpansionPanelOneLine, MDExpansionPanel
from kivymd import images_path

root_kv = """
#:import get_hex_from_color kivy.utils.get_hex_from_color


<Content>:
    orientation: "vertical"
    padding: dp(10)
    spacing: dp(10)
    size_hint_y: None
    height: self.minimum_height

    TwoLineIconListItem:
        text: "(050)-123-45-67"
        secondary_text:
            "Mobile" 

        IconLeftWidget:
            icon: "phone"

    TwoLineIconListItem:
        text: "kivydevelopment@gmail.com"
        secondary_text:
            "Work"

        IconLeftWidget:
            icon: "email"


Screen:

    MDCard:
        id: card
        orientation: "vertical"
        size_hint: .6, None
        height: self.minimum_height
        pos_hint: {"center_x": .5, "center_y": .5}

        BoxLayout:
            id: box
            size_hint_y: None
            height: dp(150)

            FitImage:
                source: "demos/kitchen_sink/assets/guitar-1139397_1280.png"
"""


class Content(BoxLayout):
    pass


class MainApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "Expansion Panel with Card"
        super().__init__(**kwargs)

    def build(self):
        self.root = Builder.load_string(root_kv)

    def on_start(self):
        content = Content()
        self.root.ids.card.add_widget(
            MDExpansionPanel(
                on_open=self.panel_open,
                on_close=self.panel_close,
                icon="kivymd_logo.png",
                content=content,
                panel_cls=MDExpansionPanelOneLine(text="KivyMD v.0.103.0"),
            )
        )

    def panel_open(self, *args):
        Animation(
            height=(self.root.ids.box.height + self.root.ids.content.height)
                   - self.theme_cls.standard_increment * 2,
            d=0.2,
        ).start(self.root.ids.box)

    def panel_close(self, *args):
        Animation(
            height=(self.root.ids.box.height - self.root.ids.content.height)
                   + self.theme_cls.standard_increment * 2,
            d=0.2,
        ).start(self.root.ids.box)


MainApp().run()
