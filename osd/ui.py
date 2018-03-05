from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget

from osd.drawing import Brush, Fill, Erase, Square, Circle, Line
from osd.util import UndoStack


class OverviewScreen(Screen):
    pass


class DrawingScreen(Screen):
    pass


class ColoredButton(ToggleButton):
    color = 0

    def __init__(self, **kwargs):
        super(ColoredButton, self).__init__(**kwargs)
        Clock.schedule_once(self.init, .1)

    def init(self, _):
        self.background_color = self.getColor()

    def getColor(self):
        col = float(self.color + 1) * .3
        return [col, col, col, 1]

    def click(self):
        App.get_running_app().toolManager.selectColor(self.color)


class ImagedButton(Button):
    icon = 'resources/brush.png'
    tool = -1

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


class DrawSpace(Widget):
    tools = [None, None, None,
             Brush, Fill, Erase,
             Line, Circle, Square]
    tool = None
    selectedTool = 3
    selectedColor = 0
    touchState = False

    def __init__(self, **kwargs):
        super(DrawSpace, self).__init__(**kwargs)
        toolManager = App.get_running_app().toolManager
        toolManager.drawingModel = self
        self.stack = UndoStack(toolManager.undo, toolManager.redo)
        self.replaceTool()

    def selectTool(self, tool):
        if tool == 1:
            self.stack.undo()
        elif tool == 2:
            self.stack.redo()
        else:
            self.selectedTool = tool
            self.replaceTool()

    def selectColor(self, color):
        self.selectedColor = color
        self.replaceTool()

    def replaceTool(self):
        self.tool = self.tools[self.selectedTool](self.selectedColor, self.addInstruction, self.canvas)

    def addInstruction(self, instruction):
        self.stack.push(instruction)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.tool.press(touch)
            self.touchState = True

    def on_touch_move(self, touch):
        if self.touchState:
            self.tool.move(touch)

    def on_touch_up(self, touch):
        if self.touchState:
            self.tool.up(touch)
        self.touchState = False


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
    drawColor = 2
    eraseColor = -1
    drawingModel = None

    def undoUI(self, enable):
        screenManager.current_screen.ids.undo.disabled = not enable

    def redoUI(self, enable):
        screenManager.current_screen.ids.redo.disabled = not enable

    def selectedColor(self):
        if self.selectedTool == self.erase:
            return self.eraseColor
        else:
            return self.drawColor

    def selectTool(self, tool):
        self.selectedTool = tool
        self.eraseColor = -1
        self.updateColorSelect()
        self.drawingModel.selectTool(tool)

    def selectColor(self, color):
        if self.selectedTool == self.erase:
            if self.eraseColor == color:
                self.eraseColor = -1
            else:
                self.eraseColor = color
        else:
            self.drawColor = color
        self.drawingModel.selectColor(color)

    def updateColorSelect(self):
        for colorWidget in ColoredButton.get_widgets('color'):
            colorWidget.allow_no_selection = self.selectedTool == self.erase
            if self.selectedColor() == colorWidget.color:
                colorWidget.state = 'down'
            else:
                colorWidget.state = 'normal'
        self.drawingModel.selectColor(self.selectedColor())


screenManager = ScreenManager()


class PanPrintApp(App):
    toolManager = ToolManager()

    def build(self):
        self.title = 'Pannenkoekenswag'

        screenManager.add_widget(DrawingScreen(name='drawing'))
        screenManager.add_widget(OverviewScreen(name='overview'))

        screenManager.current = 'overview'
        return screenManager


# Window.fullscreen = 'auto'
Window.size = (1024, 600)
PanPrintApp().run()
