from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget


class OverviewScreen(Screen):
    pass


class DrawingScreen(Screen):
    pass


class ColoredButton(Button):
    color = 0

    def getColor(self):
        return [[9, .9, .9, 1],
                [.6, .6, .6, 1],
                [.3, .3, .3, 1]][self.color]

    def click(self):
        App.get_running_app().toolManager.selectColor(self.color)


class ImagedButton(Button):
    icon = 'resources/brush.png'
    tool = -1

    def build(self):
        pass

    def click(self):
        App.get_running_app().toolManager.selectTool(self.tool)
        self.icon = 'resources/erase.png'
        print(self.icon)
        print(self.tool)


class DrawSpace(Widget):
    def build(self):
        pass


class ToolManager:
    panprint = 0
    undo = 1
    redo = 2
    brush = 3
    fill = 4
    erase = 5
    line = 6
    circle = 7
    square = 8
    selectedTool = brush
    selectedColor = 0

    def selectTool(self, tool):
        self.selectedTool = tool
        print('tool selected: ' + str(tool))

    def selectColor(self, color):
        if self.selectedColor == color:
            self.selectedColor = -1
            print('color selected: -1')
        else:
            self.selectedColor = color
            print('color selected: ' + str(color))


screenManager = ScreenManager()

screenManager.add_widget(DrawingScreen(name='drawing'))
screenManager.add_widget(OverviewScreen(name='overview'))

screenManager.current = 'drawing'


class PanPrintApp(App):
    toolManager = ToolManager()

    def build(self):
        self.title = 'Pannenkoekenswag'
        return screenManager


# Window.fullscreen = 'auto'
Window.size = (1024, 600)
PanPrintApp().run()
