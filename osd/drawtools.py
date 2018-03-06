import math

from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line


class Tool:
    def __init__(self, drawspace):
        self.drawspace = drawspace

    @property
    def color(self):
        return .3 * float(self.drawspace.selectedColor + 1)

    @property
    def width(self):
        return self.drawspace.selectedWidth

    @property
    def canvas(self):
        return self.drawspace.canvas

    def activate(self):
        return True

    def down(self, touch):
        pass

    def move(self, touch):
        pass

    def up(self, touch):
        pass


class Instruction:
    def __init__(self, color, instruction):
        self.color = color
        self.instruction = instruction


class UndoTool(Tool):
    def activate(self):
        drawobj = self.drawspace.stack.undo()
        self.drawspace.canvas.remove(drawobj.instruction)
        return False


class RedoTool(Tool):
    def activate(self):
        drawobj = self.drawspace.stack.redo()
        col = .3 * float(drawobj.color + 1)
        self.drawspace.canvas.add(Color(col, col, col))
        self.drawspace.canvas.add(drawobj.instruction)
        return False


class BrushTool(Tool):
    line = None

    def down(self, touch):
        with self.canvas:
            Color(self.color, self.color, self.color)
            self.line = Line(width=self.width, points=(touch.x, touch.y))

    def move(self, touch):
        self.line.points += (touch.x, touch.y)

    def up(self, _):
        self.drawspace.addInstruction(self.line)


class FillTool(Tool):
    pass


class EraseTool(BrushTool):
    @property
    def color(self):
        return 0


class LineTool(Tool):
    line = None
    start = (0, 0)

    def down(self, touch):
        with self.canvas:
            Color(self.color, self.color, self.color)
            self.start = (touch.x, touch.y)
            self.line = Line(width=self.width, points=self.start + self.start)

    def move(self, touch):
        self.line.points = self.start + (touch.x, touch.y)

    def up(self, _):
        self.drawspace.addInstruction(self.line)


class CircleTool(Tool):
    line = None
    center = (0, 0)

    @property
    def area(self):
        return self.drawspace.area

    def down(self, touch):
        with self.canvas:
            Color(self.color, self.color, self.color)
            self.center = (touch.x, touch.y)
            self.line = Line(width=self.width, circle=self.center + (0,))

    def move(self, touch):
        maxradius = min(self.center[0] - self.area.x,
                        self.area.x + self.area.width - self.center[0],
                        self.center[1] - self.area.y,
                        self.area.y + self.area.height - self.center[1]) - self.width
        radius = math.sqrt(abs(self.center[0] - touch.x) ** 2 + abs(self.center[1] - touch.y) ** 2)
        self.line.circle = self.center + (min(radius, maxradius),)

    def up(self, _):
        self.drawspace.addInstruction(self.line)


class SquareTool(Tool):
    line = None
    start = (0, 0)

    def down(self, touch):
        with self.canvas:
            Color(self.color, self.color, self.color)
            self.start = (touch.x, touch.y)
            self.line = Line(width=self.width, points=self.start + self.start)

    def move(self, touch):
        self.line.points = self.start + (self.start[0], touch.y) + (touch.x, touch.y) + \
                           (touch.x, self.start[1]) + self.start

    def up(self, _):
        self.drawspace.addInstruction(self.line)
