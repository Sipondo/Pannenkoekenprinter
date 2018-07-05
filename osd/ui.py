from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager

from drawtoolmanager import ToolManager


class OverviewScreen(Screen):
    def goto(self, screen):
        pass


class DrawingScreen(Screen):
    pass


class PanPrintApp(App):
    toolManager = ToolManager()
    screenManager = ScreenManager()

    def build(self):
        self.title = 'Pannenkoekenswag'

        self.screenManager.add_widget(OverviewScreen(name='overview'))
        self.screenManager.current = 'overview'

        self.screenManager.add_widget(DrawingScreen(name='drawing'))

        return self.screenManager


Window.fullscreen = True
# Window.size = (1024, 600)
PanPrintApp().run()
