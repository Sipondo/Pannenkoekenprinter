class Tool:
    def __init__(self, drawspace):
        self.drawspace = drawspace

    @property
    def color(self):
        return self.drawspace.selectedColor

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
