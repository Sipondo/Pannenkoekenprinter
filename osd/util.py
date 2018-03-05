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
            self.stack += x
            self.sp += 1
        else:
            self.stack[self.sp] = x
            self.sp += 1
            if self.full():
                self.redoCallback(False)

    def undo(self):
        if self.full():
            self.redoCallback(True)
        if not self.empty():
            self.sp -= 1
        if self.empty():
            self.undoCallback(False)

    def redo(self):
        if self.empty():
            self.undoCallback(True)
        if not self.full():
            self.sp += 1
        if self.full():
            self.redoCallback(False)
