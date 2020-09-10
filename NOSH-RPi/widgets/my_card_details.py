from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import HoverBehavior, TouchBehavior, FocusBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.taptargetview import MDTapTargetView

from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine, MDExpansionPanelThreeLine, \
    MDExpansionChevronRight
from kivymd.uix.list import OneLineIconListItem, OneLineListItem
from kivymd.uix.label import MDLabel
from kivymd.utils.fitimage import FitImage
from kivymd.theming import ThemableBehavior
from kivy.animation import Animation, AnimationTransition
from kivymd.uix.behaviors import MagicBehavior
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import ButtonBehavior


class MyImageWidget(FitImage, MagicBehavior):
    def __init__(self, image_path, **kwargs):
        super().__init__(**kwargs)

        self.source = image_path

    def grow_widget(self):
        """Grow effect animation."""
        Animation.stop_all(self)
        (
            Animation(scale_x=1, scale_y=1, t="out_circ", d=0.5)
        ).start(self)

    def shrink_widget(self):
        """Shrink effect animation."""

        Animation.stop_all(self)
        (
            Animation(scale_x=0.9, scale_y=0.9, t="out_circ", d=0.5)
        ).start(self)


class MyCardWidget(MDGridLayout):

    def __init__(self, header_text, image_path, **kwargs):
        super(MyCardWidget, self).__init__(**kwargs)

        self.header_text = header_text
        self.image_path = image_path

        self.card_widget = MyCard(header_text=self.header_text,
                                  image_source=image_path)

        self.add_widget(self.card_widget)


class MyCardContent(MDBoxLayout):

    def __init__(self, content_text, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(OneLineListItem(text=content_text))


class MyExpansionPanel(MDExpansionPanel):
    def __init__(self, header_text, **kwargs):
        self.panel_cls = MDExpansionPanelOneLine(text=header_text)
        super().__init__(**kwargs)
        self.on_open = self.panel_open
        self.on_close = self.panel_close
        self.id = 'card_expansion_panel'
        self.content = MyCardContent(content_text='')
        self.initial_height = self.height
        self.increment = self.initial_height / 2
        self.animation_duration = 0.2

    def panel_open(self, *args):
        Animation(height=(self.initial_height + self.increment),
                  d=self.animation_duration).start(self)

    def panel_close(self, *args):
        Animation(height=self.initial_height,
                  d=self.animation_duration).start(self)


class MyCard(MDCard, MagicBehavior):
    def __init__(self, header_text, image_source, **kwargs):
        super().__init__(**kwargs)
        self.id = 'card'
        self.expansion_panel_widget = MyExpansionPanel(header_text=header_text)
        self.image_widget = MyImageWidget(image_path=image_source)
        self.ids.box.add_widget(self.image_widget)

        self.add_widget(self.expansion_panel_widget)

    def on_enter(self):
        self.expansion_panel_widget.panel_open()
        self.image_widget.shrink_widget()

    def on_leave(self):
        self.expansion_panel_widget.panel_close()
        self.image_widget.grow_widget()
