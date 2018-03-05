from kivy.app import App
from kivy.uix.widget import Widget

from osd.util import UndoStack


class Tool:
    def __init__(self, color, addInstruction, canvas):
        self.color = color
        self.addInstruction = addInstruction
        self.canvas = canvas

    def press(self, touch):
        pass

    def move(self, touch):
        pass

    def release(self, touch):
        pass


class Brush(Tool):
    line = None

    def press(self, touch):
        col = .3 * float(self.color + 1)
        with self.canvas:
            self.line = Line(points=(touch.x, touch.y))

    def move(self, touch):
        self.line.points += (touch.x, touch.y)


class Fill(Tool):
    pass


class Erase(Brush):
    pass


class Line(Tool):
    pass


class Circle(Tool):
    pass


class Square(Tool):
    pass


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
