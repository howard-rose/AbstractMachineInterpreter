from tape import *


class Machine:
    def __init__(self, memory=None, tapes=None, states=None):
        self.memory = {} if memory is None else memory
        self.tapes = {} if tapes is None else tapes
        self.states = {} if states is None else states

        self.input = self.tapes[next(iter(self.tapes))] if self.tapes else Tape()
        self.output = Tape()