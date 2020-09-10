from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.carousel import MDCarousel
from kivymd.utils.fitimage import FitImage
from widgets import MyImageWidget
from kivymd.uix.behaviors import *
from kivymd.uix.button import ButtonBehavior


class MyImageDetailsWidget(MDBoxLayout):
    def __init__(self, image_path, **kwargs):
        super().__init__(**kwargs)

        self.image_widget = MyImageWidget(image_path=image_path)

        self.add_widget(self.image_widget)

    def grow(self):
        self.image_widget.grow_widget()


class MyCarousel(MDCarousel, FocusBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MyImageDetailsWidget(id='upma', image_path='resources/upma.png'))
        self.add_widget(MyImageDetailsWidget(id='dal', image_path='resources/dal_fry.png'))
        self.add_widget(MyImageDetailsWidget(id='channa', image_path='resources/channa_masala.png'))

    def on_slide_complete(self, *args):
        print("slide complete")
        print(self.index)


class CookScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        print(self.ids.my_carousel.size)
