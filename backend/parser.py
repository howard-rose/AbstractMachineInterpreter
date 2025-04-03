from backend.machine import *
import re
import json


def parse_data(lines):
    memory = {}
    tapes = {}

    for line in lines:
        match line.rstrip().split():
            case 'STACK', name:
                memory[name] = Stack()
            case 'QUEUE', name:
                memory[name] = Queue()
            case 'TAPE', name:
                tapes[name] = Tape()
            case '2D_TAPE', name:
                tapes[name] = Tape2D()

    return memory, tapes


def parse_logic(lines):
    logic_regex = re.compile(
        r'^(?P<state>\w+)] (?P<command>\w+(?: RIGHT| LEFT)?)(?:\((?P<arg>\w+)\))? (?P<transitions>.*)$')
    transition_regex = re.compile(r'\((?P<symbol>\S+),(?P<state>\S+)\)')
    overwrite_regex = re.compile(r'\((?P<symbol>\S+)/(?P<overwrite>\S+),(?P<state>\S+)\)')

    states = {}

    for line in lines:
        l_match = logic_regex.match(line)
        if l_match:
            # print(l_match.groupdict())
            # print(l_match['transitions'].split(', '))

            transitions = defaultdict(lambda: ['reject'])
            overwrites = defaultdict(lambda: [None]) if l_match['command'] == 'LEFT' or l_match['command'] == 'RIGHT' else None

            for t in l_match['transitions'].split(', '):
                if l_match['command'] == 'LEFT' or l_match['command'] == 'RIGHT':
                    t_match = overwrite_regex.match(t)

                    if t_match['symbol'] not in overwrites:
                        overwrites[t_match['symbol']] = []
                    overwrites[t_match['symbol']].append(t_match['overwrite'])
                else:
                    t_match = transition_regex.match(t)

                if t_match['symbol'] not in transitions:
                    transitions[t_match['symbol']] = []
                transitions[t_match['symbol']].append(t_match['state'])

            state = State(
                command=l_match['command'],
                transitions=transitions,
                receiver=l_match['arg'],
                overwrites=overwrites
            )

            # print(state, end='\n\n')

            states[l_match['state']] = state

    return states


def parse(stream):
    lines = list(stream)

    logic_index = lines.index('.LOGIC\n')
    data_section, logic_section = lines[:logic_index], lines[logic_index:]

    memory, tapes = parse_data(data_section)
    states = parse_logic(logic_section)

    # print(memory)
    # print(tapes)
    # for k, v in states.items():
    #     print(f'{k}: {v}')

    return Machine(states, memory, tapes)


if __name__ == '__main__':
    with open('sample_machines/sample5.txt', 'r') as machine_input:
        machine = parse(machine_input)
        machine.timelines[0].input.set_tape('aaaabbbbcccc')

        while not machine.verdict:
            #input()
            machine.step()
            for tl in machine.timelines:
                print(tl)
                print(f'Current state: {tl.state} -> {machine.states[tl.state] if tl.state != 'reject' and tl.state != 'accept' else ''}')
                print(tl.input)
                print(tl.input.head * ' ' + '^')

        print(json.dumps(machine, default=vars))