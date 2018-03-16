from drawtoolcontrol import Tool

_fourIter = [(1, 0), (0, 1), (-1, 0), (0, -1)]
_eightIter = [(-1, 0), (-1, -1), (0, -1), (-1, 1), (0, 0), (1, -1), (0, 1), (1, 1), (1, 0)]


def fourIter(x, y):
    for (dx, dy) in _fourIter:
        yield (x + dx, y + dy)


def eightIter(x, y, dx, dy):
    next = (-dx, -dy)
    for _ in range(7):
        next = _eightIter[next[0] + 3 * next[1] + 4]
        yield next


class FillTool(Tool):
    fillArea = None
    fillShapes = None
    searchColor = None

    @property
    def area(self):
        return self.drawspace.area

    def pixel(self, x, y):
        return self.canvas.get_pixel_color(x + self.area.x, y + self.area.y)

    def down(self, touch):
        self.fillArea = [[0 for _ in range(600)] for _ in range(600)]
        self.fillShapes = []
        self.searchColor = self.pixel(touch.x, touch.y)
        self.dfs(touch.x, touch.y)

    def dfs(self, x, y):
        if self.pixel(x, y) != self.searchColor:
            return
