import copy
from dataclasses import dataclass

from backend.memory_object import *
from backend.tape import *


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
    def __init__(self, states, memory=None, tapes=None, input=None):
        self.states = states
        self.initial = Timeline(
            memory=memory if memory else {},
            tapes=tapes if tapes else {},
            input=tapes[next(iter(tapes))] if tapes else Tape(),
            output='',
            state=next(iter(states))
        )

        self.verdict = None
        self.timelines = [copy.deepcopy(self.initial)]
        if input:
            self.timelines[0].input.set_tape(input)

    def reset(self, input):
        self.verdict = None
        self.timelines = [copy.deepcopy(self.initial)]
        if input:
            self.timelines[0].input.set_tape(input)

    def step(self):
        if self.verdict:
            print(self.verdict)
            return

        new_timelines = []

        for timeline in self.timelines:
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
                    try:
                        symbol = new_tl.memory[curr_state.receiver].read()
                        next_states = curr_state.transitions[symbol]
                    except IndexError:
                        next_states = ['reject']
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
                    overwrites = curr_state.overwrites[symbol]
                    next_states = curr_state.transitions[symbol]
                    for state, overwrite in zip(next_states, overwrites):
                        temp_new_tl = copy.deepcopy(new_tl)
                        temp_new_tl.state = state
                        if overwrite:
                            temp_new_tl.tapes[curr_state.receiver].write(overwrite)
                        new_timelines.append(temp_new_tl)
                case 'LEFT':
                    new_tl.tapes[curr_state.receiver].left()
                    symbol = new_tl.tapes[curr_state.receiver].scan()
                    overwrites = curr_state.overwrites[symbol]
                    next_states = curr_state.transitions[symbol]
                    for state, overwrite in zip(next_states, overwrites):
                        temp_new_tl = copy.deepcopy(new_tl)
                        temp_new_tl.state = state
                        if overwrite:
                            temp_new_tl.tapes[curr_state.receiver].write(overwrite)
                        new_timelines.append(temp_new_tl)
                case 'UP':
                    new_tl.tapes[curr_state.receiver].up()
                    symbol = new_tl.tapes[curr_state.receiver].scan()
                    overwrites = curr_state.overwrites[symbol]
                    next_states = curr_state.transitions[symbol]
                    for state, overwrite in zip(next_states, overwrites):
                        temp_new_tl = copy.deepcopy(new_tl)
                        temp_new_tl.state = state
                        if overwrite:
                            temp_new_tl.tapes[curr_state.receiver].write(overwrite)
                        new_timelines.append(temp_new_tl)
                case 'DOWN':
                    new_tl.tapes[curr_state.receiver].down()
                    symbol = new_tl.tapes[curr_state.receiver].scan()
                    overwrites = curr_state.overwrites[symbol]
                    next_states = curr_state.transitions[symbol]
                    for state, overwrite in zip(next_states, overwrites):
                        temp_new_tl = copy.deepcopy(new_tl)
                        temp_new_tl.state = state
                        if overwrite:
                            temp_new_tl.tapes[curr_state.receiver].write(overwrite)
                        new_timelines.append(temp_new_tl)

        for timeline in new_timelines:
            if timeline.state == 'accept' or (timeline.state == 'reject' and self.verdict != 'accept'):
                self.verdict = timeline.state
                print(self.verdict)

        self.timelines = new_timelines
