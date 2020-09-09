from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import HoverBehavior, TouchBehavior, FocusBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.taptargetview import MDTapTargetView

from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine, MDExpansionPanelThreeLine, MDExpansionChevronRight

from kivymd.uix.label import MDLabel
from kivymd.utils.fitimage import FitImage
from kivymd.theming import ThemableBehavior
from kivy.animation import Animation, AnimationTransition
from kivymd.uix.behaviors import MagicBehavior
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.snackbar import Snackbar


class MyImageWidget(FitImage, MagicBehavior):
    def __init__(self, image_path, **kwargs):
        super().__init__(**kwargs)

        self.source = image_path

    def grow_widget(self):
        """Grow effect animation."""

        Animation.stop_all(self)
        (
            Animation(scale_x=1.2, scale_y=1.2, t="out_circ", d=1.)
        ).start(self)

    def shrink_widget(self):
        """Shrink effect animation."""

        Animation.stop_all(self)
        (
            Animation(scale_x=1.0, scale_y=1.0, t="out_circ", d=1.)
        ).start(self)


class MyLabel(MDLabel):
    def __init__(self, content, **kwargs):
        super().__init__(**kwargs)
        self.text = content


class MyCardWidget(MDGridLayout, HoverBehavior):

    def __init__(self, header_text, content_text, image_path, **kwargs):
        super(MyCardWidget, self).__init__(**kwargs)

        self.header_text = header_text
        self.content_text = content_text
        self.image_path = image_path


        # initialize widgets

        self.image_widget = MyImageWidget(image_path=self.image_path)
        self.label_widget = MyLabel(id='label1', content=self.content_text)
        self.snackbar_widget = Snackbar(text=self.content_text, padding="20dp", duration=1)

        self.add_widget(self.image_widget)

    def on_enter(self, *args):
        '''The method will be called when the mouse cursor
        is within the borders of the current widget.'''

        self.image_widget.grow_widget()
        self.snackbar_widget.show()

    def on_leave(self, *args):
        '''The method will be called when the mouse cursor goes beyond
        the borders of the current widget.'''

        self.image_widget.shrink_widget()

    def tap_target_start(self):
        if self.tap_target_view.state == "close":
            self.tap_target_view.start()
        else:
            self.tap_target_view.stop()


class MyCardContent(MDBoxLayout):

    def __init__(self, content_text, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(MDLabel(text=content_text))
