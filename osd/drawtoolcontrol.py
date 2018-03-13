from kivy.graphics.context_instructions import Color

from drawtoolabstract import Tool


class UndoTool(Tool):
    def activate(self):
        drawobj = self.drawspace.stack.undo()
        self.drawspace.canvas.remove(drawobj.instruction)
        return False


class RedoTool(Tool):
    def activate(self):
        drawobj = self.drawspace.stack.redo()
        col = drawobj.color
        self.drawspace.canvas.add(Color(col[0], col[1], col[2]))
        self.drawspace.canvas.add(drawobj.instruction)
        return False
