from dataclasses import dataclass

from memory_object import *
from tape import *


@dataclass
class State:
    command: str
    transitions: dict[str, list[str]] = None
    receiver: str | None = None
    overwrites: dict[str, list[str]] = None


@dataclass
class Timeline:
    memory: dict[str, MemoryObject]
    tapes: dict[str, Tape]
    input: Tape
    output: str
    state: str


class Machine:
    def __init__(self, states, memory=None, tapes=None):
        self.states = states
        self.timelines = [Timeline(
            memory=memory if memory else {},
            tapes=tapes if tapes else {},
            input=tapes[next(iter(tapes))] if tapes else Tape(),
            output='',
            state=next(iter(states))
        )]

    def step(self):
        for timeline in self.timelines:
            curr_state = self.states[timeline.state]
            match curr_state.command:
                case 'SCAN' | 'SCAN RIGHT':
                    timeline.input.right()
                    symbol = timeline.input.scan()
                case 'SCAN LEFT':
                    timeline.input.left()
                    symbol = timeline.input.scan()
                case 'PRINT':
                    symbols = []
                    for transition in curr_state.transitions:
                        symbols.append(transition)
                case 'READ':
                    pass
                case 'WRITE':
                    pass
                case 'RIGHT':
                    pass
                case 'LEFT':
                    pass
                case 'UP':
                    pass
                case 'DOWN':
                    pass

    # def scan_right(self):
    #     self.input.right()
    #     symbol = self.input.scan()
    #
    # def scan_left(self):
    #     self.input.left()
    #     symbol = self.input.scan()
    #
    # def print(self):
    #     pass
    #
    # def read(self, mem):
    #     symbol = self.memory.read(mem)
    #
    # def write(self, mem, symbol):
    #     self.memory.write(mem, symbol)
