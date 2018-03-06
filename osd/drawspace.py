from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget

from osd.drawtools import Instruction
from osd.util import UndoStack, Area, bindArea


class DrawSpace(Widget):
    selectedTool = None
    selectedColor = 0
    selectedWidth = 0

    touchState = False
    stack = None

    def __init__(self, **kwargs):
        super(DrawSpace, self).__init__(**kwargs)
        Clock.schedule_once(self.init, .1)

    def init(self, _):
        toolManager = App.get_running_app().toolManager
        toolManager.setDrawspace(self)
        self.stack = UndoStack(toolManager.undoUI, toolManager.redoUI)

    __area = None

    @property
    def area(self):
        if self.__area is None:
            self.__area = Area(self.x, self.y, self.width, self.height)
        return self.__area

    def selectTool(self, tool):
        self.selectedTool = tool

    def selectColor(self, color):
        self.selectedColor = color

    def selectWidth(self, width):
        self.selectedWidth = width

    def addInstruction(self, instruction):
        self.stack.push(Instruction(self.selectedColor, instruction))

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.selectedTool.down(bindArea(touch, self.area, self.selectedWidth))
            self.touchState = True

    def on_touch_move(self, touch):
        if self.touchState:
            self.selectedTool.move(bindArea(touch, self.area, self.selectedWidth))

    def on_touch_up(self, touch):
        if self.touchState:
            self.selectedTool.up(bindArea(touch, self.area, self.selectedWidth))
        self.touchState = False
