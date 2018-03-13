class UndoStack:
    stack = []
    sp = 0

    def __init__(self, undoCallback, redoCallback):
        self.undoCallback = undoCallback
        self.redoCallback = redoCallback

    def full(self):
        return self.sp == len(self.stack)

    def empty(self):
        return self.sp == 0

    def push(self, x):
        if self.empty():
            self.undoCallback(True)
        if self.full():
            self.stack += [x]
            self.sp += 1
        else:
            self.stack[self.sp] = x
            self.sp += 1
            if self.full():
                self.redoCallback(False)
            else:
                del self.stack[self.sp:]

    def undo(self):
        if self.full():
            self.redoCallback(True)
        if not self.empty():
            self.sp -= 1
            if self.empty():
                self.undoCallback(False)
            return self.stack[self.sp]
        return None

    def redo(self):
        if self.empty():
            self.undoCallback(True)
        if not self.full():
            self.sp += 1
            if self.full():
                self.redoCallback(False)
            return self.top()

    def top(self):
        if self.sp == 0:
            return None
        return self.stack[self.sp - 1]


class Pos:
    def __init__(self, x, y, baseX, baseY):
        self.x = x
        self.y = y
        self.baseX = baseX
        self.baseY = baseY


class Area:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h

    @property
    def xf(self):
        return self.x + self.width

    def yf(self):
        return self.y + self.height


def bindArea(p, a, padding):
    pos = Pos(p.x, p.y, p.x, p.y)
    if p.x < a.x + padding:
        pos.x = a.x + padding
    if p.y < a.y + padding:
        pos.y = a.y + padding
    if p.x > a.x + a.width - padding:
        pos.x = a.x + a.width - padding
    if p.y > a.y + a.height - padding:
        pos.y = a.y + a.height - padding
    return pos


def normalize(pos):
    pos.x -= pos.baseX
    pos.y -= pos.baseY
    pos.baseX = 0
    pos.baseY = 0
    return pos
