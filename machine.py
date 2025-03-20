class Machine:
    def __init__(self, memory=None, tapes=None, states=None):
        self.memory = {} if memory is None else memory
        self.tapes = {} if tapes is None else tapes
        self.states = {} if states is None else states