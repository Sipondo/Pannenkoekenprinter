from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager

from osd.toolmanager import ToolManager


class OverviewScreen(Screen):
    pass


class DrawingScreen(Screen):
    pass


screenManager = ScreenManager()


class PanPrintApp(App):
    toolManager = ToolManager(screenManager)

    def build(self):
        self.title = 'Pannenkoekenswag'

        screenManager.add_widget(DrawingScreen(name='drawing'))
        screenManager.add_widget(OverviewScreen(name='overview'))

        screenManager.current = 'overview'
        return screenManager


Window.fullscreen = False
Window.size = (1024, 600)
PanPrintApp().run()
