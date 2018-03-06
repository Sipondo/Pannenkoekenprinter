from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager

from osd.drawtoolmanager import ToolManager


class OverviewScreen(Screen):
    pass


class DrawingScreen(Screen):
    pass


class PanPrintApp(App):
    toolManager = ToolManager()
    screenManager = ScreenManager()

    def build(self):
        self.title = 'Pannenkoekenswag'

        self.screenManager.add_widget(DrawingScreen(name='drawing'))
        self.screenManager.add_widget(OverviewScreen(name='overview'))

        self.screenManager.current = 'overview'
        return self.screenManager


Window.fullscreen = False
Window.size = (1024, 600)
PanPrintApp().run()
