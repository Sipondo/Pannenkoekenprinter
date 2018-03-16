from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton


class ImagedButton(Button):
    icon = 'resources/brush.png'
    tool = None

    def __init__(self, **kwargs):
        super(ImagedButton, self).__init__(**kwargs)
        Clock.schedule_once(self.init, .1)

    def init(self, _):
        self.children[0].source = self.icon

    def click(self):
        App.get_running_app().toolManager.selectTool(self.tool)


class ImagedToolButton(ToggleButton):
    icon = 'resources/brush.png'
    tool = -1

    def __init__(self, **kwargs):
        super(ImagedToolButton, self).__init__(**kwargs)
        Clock.schedule_once(self.init, .1)

    def init(self, _):
        self.children[0].source = self.icon

    def click(self):
        App.get_running_app().toolManager.selectTool(self.tool)


class ColoredButton(ToggleButton):
    color = [0, 0, 0, 0]

    def __init__(self, **kwargs):
        super(ColoredButton, self).__init__(**kwargs)
        Clock.schedule_once(self.init, .1)

    def init(self, _):
        self.background_color = self.color

    def click(self):
        App.get_running_app().toolManager.selectColor(self.color)


class MenuButton(Button):
    icon = 'resources/brush.png'
    screen = 'overview'

    def __init__(self, **kwargs):
        super(MenuButton, self).__init__(**kwargs)
        Clock.schedule_once(self.init, .1)

    def init(self, _):
        self.children[0].source = self.icon

    def click(self):
        App.get_running_app().screenManager.current = self.screen
