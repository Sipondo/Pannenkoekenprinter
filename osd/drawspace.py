from drawtoolabstract import Instruction
from drawtooldraw import EraseTool
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from util import Area, UndoStack, bindArea


class DrawSpace(Widget):
    selectedTool = None
    selectedColor = 0
    selectedWidth = 0

    touchState = False
    stack = None
    area = None

    def __init__(self, **kwargs):
        super(DrawSpace, self).__init__(**kwargs)
        Clock.schedule_once(self.init, .1)

    _area = None

    @property
    def area(self):
        if self._area is None:
            self._area = Area(self.x, self.y, self.width, self.height)
        return self._area

    def init(self, _):
        toolManager = App.get_running_app().toolManager
        toolManager.setDrawspace(self)
        self.stack = UndoStack(toolManager.undoUI, toolManager.redoUI)

    def selectTool(self, tool):
        self.selectedTool = tool

    def selectColor(self, color):
        self.selectedColor = color

    def selectWidth(self, width):
        self.selectedWidth = width

    def addInstruction(self, instruction):
        if type(self.selectedTool) is EraseTool:
            color = -1
        else:
            color = self.selectedColor
        self.stack.push(Instruction(color, instruction))

    def on_touch_down(self, touch):
        touch = self.fix_touch(touch)
        if self.collide_point(touch.x, touch.y):
            self.selectedTool.down(bindArea(touch, self.area, self.selectedWidth))
            self.touchState = True

    def on_touch_move(self, touch):
        touch = self.fix_touch(touch)
        if self.touchState:
            self.selectedTool.move(bindArea(touch, self.area, self.selectedWidth))

    def on_touch_up(self, touch):
        touch = self.fix_touch(touch)
        if self.touchState:
            self.selectedTool.up(bindArea(touch, self.area, self.selectedWidth))
        self.touchState = False

    def fix_touch(self, touch):
        if touch.x is not None and touch.y is not None:
        touch.x = 1024 - touch.x
        touch.y = 600 - touch.y

    def clear(self):
        self.canvas.clear()
        self.init(0)
