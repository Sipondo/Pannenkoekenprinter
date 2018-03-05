from osd.button import ColoredButton


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

    def __init__(self, sm):
        self.screenManager = sm

    def undoUI(self, enable):
        self.screenManager.current_screen.ids.undo.disabled = not enable

    def redoUI(self, enable):
        self.screenManager.current_screen.ids.redo.disabled = not enable

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
