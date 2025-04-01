import copy
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
        new_timelines = []

        while self.timelines:
            timeline = self.timelines.pop()
            curr_state = self.states[timeline.state]
            new_tl = copy.deepcopy(timeline)

            match curr_state.command:
                case 'SCAN' | 'SCAN RIGHT':
                    new_tl.input.right()
                    symbol = new_tl.input.scan()
                    next_states = curr_state.transitions[symbol]
                    for state in next_states:
                        temp_new_tl = copy.deepcopy(new_tl)
                        temp_new_tl.state = state
                        new_timelines.append(temp_new_tl)
                case 'SCAN LEFT':
                    new_tl.input.left()
                    symbol = new_tl.input.scan()
                    next_states = curr_state.transitions[symbol]
                    for state in next_states:
                        temp_new_tl = copy.deepcopy(new_tl)
                        temp_new_tl.state = state
                        new_timelines.append(temp_new_tl)
                case 'PRINT':
                    for symbol, next_states in curr_state.transitions.items():
                        for state in next_states:
                            temp_new_tl = copy.deepcopy(new_tl)
                            temp_new_tl.output += symbol
                            temp_new_tl.state = state
                            new_timelines.append(temp_new_tl)
                case 'READ':
                    new_tl.input.left()
                    symbol = new_tl.input.scan()
                    next_states = curr_state.transitions[symbol]
                    for state in next_states:
                        temp_new_tl = copy.deepcopy(new_tl)
                        temp_new_tl.state = state
                        new_timelines.append(temp_new_tl)
                case 'WRITE':
                    for symbol, next_states in curr_state.transitions.items():
                        for state in next_states:
                            temp_new_tl = copy.deepcopy(new_tl)
                            temp_new_tl.memory[curr_state.receiver].write(symbol)
                            temp_new_tl.state = state
                            new_timelines.append(temp_new_tl)
                case 'RIGHT':
                    new_tl.tapes[curr_state.receiver].right()
                    symbol = new_tl.tapes[curr_state.receiver].scan()
                    next_states = curr_state.transitions[symbol]
                    for state in next_states:
                        temp_new_tl = copy.deepcopy(new_tl)
                        temp_new_tl.state = state
                        new_timelines.append(temp_new_tl)
                case 'LEFT':
                    new_tl.tapes[curr_state.receiver].left()
                    symbol = new_tl.tapes[curr_state.receiver].scan()
                    next_states = curr_state.transitions[symbol]
                    for state in next_states:
                        temp_new_tl = copy.deepcopy(new_tl)
                        temp_new_tl.state = state
                        new_timelines.append(temp_new_tl)
                case 'UP':
                    new_tl.tapes[curr_state.receiver].up()
                    symbol = new_tl.tapes[curr_state.receiver].scan()
                    next_states = curr_state.transitions[symbol]
                    for state in next_states:
                        temp_new_tl = copy.deepcopy(new_tl)
                        temp_new_tl.state = state
                        new_timelines.append(temp_new_tl)
                case 'DOWN':
                    new_tl.tapes[curr_state.receiver].down()
                    symbol = new_tl.tapes[curr_state.receiver].scan()
                    next_states = curr_state.transitions[symbol]
                    for state in next_states:
                        temp_new_tl = copy.deepcopy(new_tl)
                        temp_new_tl.state = state
                        new_timelines.append(temp_new_tl)

        self.timelines = new_timelines

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
