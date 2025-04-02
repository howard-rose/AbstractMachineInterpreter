from collections import defaultdict


class Tape:
    def __init__(self, default_char='#'):
        if len(default_char) != 1:
            raise Exception(f'Default character must be string of length 1, got "{default_char}"')
        self.default_char = default_char
        self.tape = defaultdict(lambda: default_char)
        self.head = 0

    def __copy__(self):
        new_tape = Tape(self.default_char)
        new_tape.tape = self.tape.copy()
        new_tape.head = self.head
        return new_tape

    def __str__(self):
        s = ''
        if self.tape:
            for i in range(min(0, self.head, min(self.tape)), max(self.head, max(self.tape)) + 1):
                s += self.tape[i]
        return s + self.default_char

    def __eq__(self, other):
        return isinstance(other, Tape) and self.head == other.head and self.tape == other.tape

    def __repr__(self):
        return f'tape={self.tape} head={self.head}'

    def reset_head(self):
        self.head = 0

    def set_tape(self, content: str):
        self.tape.clear()
        self.reset_head()
        for char in content:
            self.right()
            self.tape[self.head] = char
        self.reset_head()

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

    def up(self):
        raise NotImplementedError

    def down(self):
        raise NotImplementedError


class Tape2D(Tape):
    def __init__(self):
        super().__init__()
        self.head = (0, 0) # x, y

    def __str__(self):
        keys = list(self.tape)
        keys.append(self.head)
        x_vals, y_vals = zip(*keys)

        x_min, x_max = min(0, min(x_vals)), max(x_vals)
        y_min, y_max = min(0, min(y_vals)), max(y_vals)

        s = ''
        for y in range(y_max, y_min - 1, -1):
            for x in range(x_min, x_max + 1):
                s += self.tape[x, y]
            s += self.default_char + '\n'

        return s[:-1]

    def reset_head(self):
        self.head = (0, 0)

    def right(self):
        self.head = (self.head[0] + 1, self.head[1])

    def left(self):
        self.head = (self.head[0] - 1, self.head[1])

    def up(self):
        self.head = (self.head[0], self.head[1] + 1)

    def down(self):
        self.head = (self.head[0], self.head[1] - 1)
