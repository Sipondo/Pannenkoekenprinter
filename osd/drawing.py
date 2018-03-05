from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.uix.widget import Widget

from osd.util import UndoStack, Area, bindArea


class Tool:
    def __init__(self, color, width, addInstruction, canvas):
        self.color = color
        self.width = width
        self.addInstruction = addInstruction
        self.canvas = canvas

    def down(self, touch):
        pass

    def move(self, touch):
        pass

    def up(self, touch):
        pass


class BrushTool(Tool):
    line = None

    def down(self, touch):
        col = .3 * float(self.color + 1)
        with self.canvas:
            Color(col, col, col)
            self.line = Line(width=self.width, points=(touch.x, touch.y))

    def move(self, touch):
        self.line.points += (touch.x, touch.y)

    def up(self, _):
        self.addInstruction(self.line)


class FillTool(Tool):
    pass


class EraseTool(BrushTool):
    def __init__(self, color, width, addInstruction, canvas):
        super(EraseTool, self).__init__(-1, width, addInstruction, canvas)


class LineTool(Tool):
    pass


class CircleTool(Tool):
    pass


class SquareTool(Tool):
    pass


class DrawSpace(Widget):
    tools = [None, None, None,
             BrushTool, FillTool, EraseTool,
             LineTool, CircleTool, SquareTool]
    tool = None
    selectedTool = 3
    selectedColor = 0
    touchState = False
    selectedWidth = 1

    def __init__(self, **kwargs):
        super(DrawSpace, self).__init__(**kwargs)
        toolManager = App.get_running_app().toolManager
        toolManager.drawingModel = self
        self.stack = UndoStack(toolManager.undoUI, toolManager.redoUI)
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

    def selectWidth(self, width):
        self.selectedWidth = width
        self.replaceTool()

    def replaceTool(self):
        self.tool = self.tools[self.selectedTool](self.selectedColor, self.selectedWidth, self.addInstruction,
                                                  self.canvas)

    def addInstruction(self, instruction):
        self.stack.push(instruction)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.tool.down(touch)
            self.touchState = True

    def on_touch_move(self, touch):
        if self.touchState:
            self.tool.move(bindArea(touch, Area(self.x, self.y, self.width, self.height), self.selectedWidth))

    def on_touch_up(self, touch):
        if self.touchState:
            self.tool.up(bindArea(touch, Area(self.x, self.y, self.width, self.height), self.selectedWidth))
        self.touchState = False
