from kivy.app import App

from osd.drawtools import UndoTool, SquareTool, CircleTool, LineTool, EraseTool, FillTool, BrushTool, RedoTool, Tool


class PrintTool(Tool):
    def activate(self):
        App.get_running_app().screenManager.current = 'overview'


class ToolManager:
    panprint = PrintTool
    undo = UndoTool
    redo = RedoTool
    brush = BrushTool
    fill = FillTool
    erase = EraseTool
    line = LineTool
    circle = CircleTool
    square = SquareTool

    drawspace = None

    @property
    def screenManager(self):
        return App.get_running_app().screenManager

    def setDrawspace(self, drawspace):
        from osd.const import initialTool, initialColor, initialWidth

        self.drawspace = drawspace
        self.drawspace.selectTool(initialTool(self.drawspace))
        self.drawspace.selectColor(initialColor)
        self.drawspace.selectWidth(initialWidth)

    def undoUI(self, enable):
        self.screenManager.current_screen.ids.undo.disabled = not enable

    def redoUI(self, enable):
        self.screenManager.current_screen.ids.redo.disabled = not enable

    def selectTool(self, tool):
        toolObj = tool(self.drawspace)
        if toolObj.activate():
            self.drawspace.selectTool(toolObj)

    def selectColor(self, color):
        self.drawspace.selectColor(color)

    def selectWidth(self):
        self.drawspace.selectWidth(self.screenManager.current_screen.ids.slider.value)
