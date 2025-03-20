from collections import deque


class MemoryObject(deque):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def read(self):
        return self.pop()


class Stack(MemoryObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def write(self, val):
        self.append(val)


class Queue(MemoryObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def write(self, val):
        self.appendleft(val)
