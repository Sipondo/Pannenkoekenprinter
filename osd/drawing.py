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
