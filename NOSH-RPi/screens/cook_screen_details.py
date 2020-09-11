from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.carousel import MDCarousel
from kivymd.utils.fitimage import FitImage
from widgets import MyImageWidget
from kivymd.uix.behaviors import *
from kivymd.uix.button import ButtonBehavior
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.expansionpanel import MDExpansionPanelThreeLine
from kivymd.uix.list import OneLineListItem, TwoLineListItem, ThreeLineListItem
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.graphics.texture import Texture


class MyImageDetailsWidget(MDGridLayout):
    def __init__(self, image_path, dish_name, cooking_time, **kwargs):
        super().__init__(**kwargs)

        self.cols = 2
        self.spacing = dp(5)
        self.padding = dp(5)

        # left container
        self.left_container = MDBoxLayout(orientation='vertical')
        self.left_container.spacing = dp(5)

        # right container
        self.right_container = MDBoxLayout(orientation='vertical')
        self.right_container.spacing = dp(5)

        # description item 1 card
        self.description_item1_card = MDCard(size_hint=(1.0, 0.2))

        # description item 2 card
        self.description_item2_card = MDCard(size_hint=(1.0, 0.5))

        # ingrdients table item card
        self.ingredients_table_card = MDCard(padding=dp(5),
                                             orientation='vertical')

        self.image_widget = MyImageWidget(image_path=image_path,
                                          size_hint=(1.0, 0.5))

        # description labels containing text

        self.label1 = MDLabel(
            text="""[b]Dish: {dish_name} [/b] \nTime Taken to Cook: {cooking_time} minutes""".format(
                dish_name=dish_name, cooking_time=cooking_time),
            markup=True,
            halign='left',
            valign='top'
        )

        self.description_item1_card.add_widget(self.label1)

        self.label2 = MDLabel(
            text="""[b]Description: [/b] \nUpma, uppumavu or uppittu is a dish originating from the Indian subcontinent, most common in South Indian, Maharashtrian, Odia and Sri Lankan Tamil breakfast, cooked as a thick porridge from dry-roasted semolina or coarse rice flour.""",
            markup=True,
            halign='left',
            valign='top')

        self.description_item2_card.add_widget(self.label2)

        self.ingredients_title_label = MDLabel(text="[b]Ingredients Used [/b]",
                                               markup=True,
                                               halign='center',
                                               valign='top',
                                               size_hint=(1.0, 0.1))

        self.ingredients_table = MDDataTable(use_pagination=False,
                                             column_data=[
                                                 ("Name", dp(30)),
                                                 ("Amount", dp(30)),
                                             ],
                                             row_data=[
                                                 ("Salt", "2 Tbsp"),
                                                 ("Pepper", "3 Tbsp"),
                                             ])
        self.ingredients_table_card.add_widget(self.ingredients_title_label)
        self.ingredients_table_card.add_widget(self.ingredients_table)

        # add container to card

        self.add_widget(self.left_container)
        self.add_widget(self.right_container)

        # add widgets to containers
        self.left_container.add_widget(self.image_widget)
        self.left_container.add_widget(self.description_item2_card)
        self.right_container.add_widget(self.description_item1_card)
        self.right_container.add_widget(self.ingredients_table_card)

        # self.add_widget(self.image_widget)
        # self.add_widget(self.list_item1)
        # self.add_widget(self.separator1)
        # self.add_widget(self.list_item2)
        # self.add_widget(self.label1)

    def grow(self):
        self.image_widget.grow_widget()


class MyCarousel(MDCarousel, FocusBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MyImageDetailsWidget(dish_name='Upma',
                                             cooking_time=20,
                                             image_path='resources/upma.png'))
        self.add_widget(MyImageDetailsWidget(dish_name='Dal',
                                             cooking_time=20,
                                             image_path='resources/dal_fry.png'))
        self.add_widget(MyImageDetailsWidget(dish_name='Channa',
                                             cooking_time=20,
                                             image_path='resources/channa_masala.png'))

    def on_slide_complete(self, *args):
        print("slide complete")
        print(self.index)


class CookScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
