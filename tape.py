from collections import defaultdict


class Tape:
    def __init__(self, default_char='#'):
        if len(default_char) != 1:
            raise Exception(f'Default character must be string of length 1, got "{default_char}"')
        self.tape = defaultdict(lambda: default_char)
        self.head = 0

    def scan(self) -> str:
        return self.tape[self.head]

    def write(self, char: str):
        if len(char) != 1:
            raise Exception(f'Character must be string of length 1, got "{char}"')
        self.tape[self.head] = char

    def right(self):
        self.head += 1

    def left(self):
        self.head -= 1


class Tape2D(Tape):
    def __init__(self):
        super().__init__()
        self.head = [0, 0] # x, y

    def right(self):
        self.head[0] += 1

    def left(self):
        self.head[0] -= 1

    def up(self):
        self.head[1] += 1

    def down(self):
        self.head[1] -= 1